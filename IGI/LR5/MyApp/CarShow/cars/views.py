import requests
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializers import CustomerSerializer
from django.shortcuts import render, redirect, get_object_or_404
from .models import News, CompanyInfo, Customer, Employee, Vacancy, Promocode, FAQ, Car, Order, CarType, Complete_Order, Review
from django.contrib.auth.models import User
from .forms import LoginForm, RegistryForm
from django.contrib.auth import login, logout, authenticate
from django.views import View
import datetime
from django.utils import timezone
from django.contrib.auth.decorators import login_required
import pytz
from django.core.cache import cache
import numpy
from django.db.models.functions import TruncMonth, TruncYear
from django.db.models import Sum
from collections import defaultdict
import statistics as st
import matplotlib.pyplot as plt
import io
import base64
import pandas as pd
import logging

logger = logging.getLogger('my_logger')
logger.setLevel(logging.DEBUG) 

# INFO
info_handler = logging.FileHandler('info.log')
info_handler.setLevel(logging.INFO)
info_handler.setFormatter(logging.Formatter('%(asctime)s| %(message)s'))

# ERROR
error_handler = logging.FileHandler('error.log')
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(logging.Formatter('%(asctime)s| %(message)s'))

logger.addHandler(info_handler)
logger.addHandler(error_handler)

# Create your views here.
def index (request):
    cache_key = 'daily_quote'
    quote = cache.get(cache_key)

    if not quote:
        response = requests.get('https://favqs.com/api/qotd')
        if response.status_code == 200:
            data = response.json()
            quote = data.get('quote', {}).get('body', 'No quote found')
            cache.set(cache_key, quote, timeout=86400)

    latest_news = News.objects.latest('date')
    return render(request, 'cars/index.html', {'news': latest_news, "quote": quote})

def news(request):
    news = News.objects.all().order_by('date')
    for n in news:
        end = n.text.find('.')
        if end != -1:
            n.text = n.text[:end + 1]
        else:
            n.text = n.text

    return render(request, 'cars/news.html', {'news': news})

def about(request):
    company_info = CompanyInfo.objects.last()

    return render(request, 'cars/about.html', {'comp_info': company_info})

class Registry(View):
    form_class = RegistryForm

    def post(self,req,*args,**kwargs):
        form = self.form_class(data = req.POST)
        logout(req)
        if form.is_valid():  
            user = User.objects.create_user(username=form.cleaned_data["username"],
                                            email=form.cleaned_data["email"],
                                            password=form.cleaned_data["password"],
                                            first_name=form.cleaned_data["first_name"],
                                            last_name=form.cleaned_data["last_name"],)
            
            customer = Customer.objects.create(user=user, 
                                               phone_number=form.cleaned_data["phone_number"], 
                                               birth=form.cleaned_data["birth"],
                                               time_zone = form.cleaned_data["time_zone"]) 
            
            logger.info('user {0} created'.format(user.username))
            login(req,user)
            return redirect('/')
        else:  
            logger.error('user {0} authentication error'.format(form.cleaned_data["username"]))          
            return render(req,'cars/registry.html',{"form":form,"error":form.errors.values})
        
    def get(self, req, *args, **kwargs):
        form = self.form_class()
        return render(req,'cars/registry.html',{"form":form})
    
class Login(View):
    form_class = LoginForm

    def post(self,req,*args,**kwargs):
        form = self.form_class(data = req.POST)
        logout(req)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(req, username=username, password=password)
            logger.info("user {username} try to authenticate".format(username=username))

        if user is not None:
                login(req, user)
                return redirect('/')
        else:
            logger.error('user {0} authentication error'.format(username))
            return render(req,'cars/login.html',{"form":form, "error":['Wrong username or password']})
        
    def get(self, req, *args, **kwargs):
        form = self.form_class()
        return render(req,'cars/login.html',{"form":form})
    
def car_detail(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    return render(request, 'cars/car_detail.html', {'car': car})
    
class Cars(View):
    def post(self, request, *args, **kwargs):
        car_id = request.POST.get('car_id')
        emp_id = request.POST.get('emp_id')
        quant = request.POST.get('quantity')

        if car_id and emp_id:
            car = Car.objects.get(pk=car_id)
            employee = Employee.objects.get(pk=emp_id)

            Order.objects.create(client=request.user, car=car, quantity = quant, employee = employee, 
                                 date_order=timezone.now().date())
            return redirect('/cart')
        
        else: return redirect('/')
    
    def get(self,request,*args,**kwargs):
        type_filter = request.GET.get('type')
        price_filter = request.GET.get('price')

        cars = Car.objects.all()
        employees = Employee.objects.all()
        types = CarType.objects.all()
        
        if request.user.is_anonymous: tp_us = 's'
        else:
            if Customer.objects.filter(user=request.user): tp_us = 'c' 
            else: tp_us = 's'

        if type_filter or price_filter:
            if type_filter: 
                cars = cars.filter(type=type_filter)
            if price_filter == '0': 
                cars = cars.order_by('price')
            elif price_filter == '1': 
                cars = cars.order_by('price').distinct() 
            return render(request,'cars/cars.html', {"cars": cars, "employees": employees, "types": types, "type_user": tp_us})

        return render(request, 'cars/cars.html', {"cars": cars, "employees": employees, "types": types, "type_user": tp_us})

class Cart(View):
    def post(self, request, *args, **kwargs):
        order_id = request.POST.get('order_id')
        orders = Order.objects.filter(client=request.user, is_complete=False)
        #total_price = sum(order.car.price * order.quantity for order in orders)

        if order_id:
            Order.objects.get(pk=order_id).delete()
            return redirect('/cart')

        if request.POST.get('complete_order'):
            percent = 1
            code = request.POST.get('code')
            if code != "" and Promocode.objects.filter(code=code, is_active=True): 
                promocode = Promocode.objects.get(code=code, is_active=True)
                percent = ((100 - promocode.discount) / 100)

            for order in orders:
                tot_pr = order.quantity * order.car.price * percent
                Complete_Order.objects.create(order=order, total_price=tot_pr, date_delivery=order.date_order + datetime.timedelta(days=7))
            Order.objects.filter(client=request.user).update(is_complete=True)
            return redirect('/cart')
        
        return redirect('/cart')


    def get(self, request, *args, **kwargs):
        if request.user.is_anonymous or not Customer.objects.filter(user=request.user):
            return redirect('/login')

        orders = Order.objects.filter(client=request.user, is_complete=False)
        total_price = sum(order.car.price * order.quantity for order in orders)
        return render(request, 'cars/cart.html', {"orders": orders, "total_price": total_price})

class Profile(View):
    def get(self,request,*args,**kwargs):
        if not request.user.is_authenticated:
            return redirect('/login')
        
        response = requests.get(f'https://api.genderize.io/?name={request.user.first_name}')
        if response.status_code == 200:
            data = response.json()
            gender = data.get('gender')
        else: gender = 'none'
    
        if len(Employee.objects.filter(user=request.user)) != 0:
            emp = Employee.objects.get(user=request.user)
            orders = Order.objects.filter(employee=emp, is_complete=False)
            complete_orders = Complete_Order.objects.filter(order__employee=emp)
            return render(request, 'cars/profile.html', {"orders": orders, "complete_orders": complete_orders, "type": 'e', "employee": emp, "gender": gender})
        elif len(Customer.objects.filter(user=request.user)) != 0:
            cust = Customer.objects.get(user=request.user)

            utc_time = timezone.now()
            user_tz = pytz.timezone(cust.time_zone)
            tz_time = utc_time.astimezone(tz=user_tz)

            complete_orders = Complete_Order.objects.filter(order__client=request.user)
            return render(request, 'cars/profile.html', {"complete_orders": complete_orders, "type": 'c', "customer": cust, "tz_time": tz_time, "gender": gender})
        else:
           return render(request, 'cars/profile.html', {"admin":request.user, "type": 'a', "gender": gender}) 

class Statistics(View):
    def post (self,request,*args,**kwargs):
        clients = Customer.objects.all().order_by('user__last_name')
        cars = Car.objects.all().order_by('type')

        clients_by_region = defaultdict(list)
        for client in clients:
            clients_by_region[client.time_zone].append(client)
        clients_dict = dict(clients_by_region)

        if request.POST.get('type') == 'clients': 
            return render(request, 'cars/statistics.html', {"clients": clients, "type": 'client', 'grouped_clients': clients_dict.items()})
        elif request.POST.get('type') == 'cars':
            return render(request, 'cars/statistics.html', {"cars": cars, "type": 'car'})
        else:
            return redirect('/statistics')
    
    def get(self,request,*args,**kwargs):
        complete_orders = Complete_Order.objects.all()
        clients = Customer.objects.all()
        total_price = 0
        total_quantity = 0
        prices = list()
        ages = list()
        types = list()

        for client in clients:
            age = (timezone.now().date() - client.birth).days / 365
            ages.append(age)

        ages_array = numpy.array(ages)
        mean_age = int(numpy.mean(ages_array))

        for ord in complete_orders: 
            types.append(ord.order.car.type)
            prices.append(ord.total_price)
            total_price += ord.total_price
            total_quantity += ord.order.quantity

        prices_array = numpy.array(prices)
        mean_price = numpy.mean(prices_array)
        mode_type = st.mode(types)

        profits_by_cartype = Complete_Order.objects.values(
                                                    'order__car__type__name').annotate(
                                                    total_profit=Sum('total_price')).order_by(
                                                    '-total_profit')
        profit_type = profits_by_cartype.first()['order__car__type__name']

        profits_by_car = Complete_Order.objects.values(
                                                    'order__car__name').annotate(
                                                    total_profit=Sum('total_price')).order_by(
                                                    '-total_profit')
        profit_car = profits_by_car.first()['order__car__name']
        less_profit_car = profits_by_car.last()['order__car__name']

        month_chart = sales_month_chart()
        year_chart = yearly_sales_chart()
        cus_reg_chart = region_chart()
        car_type_table = car_type_pivot_table()

        return render(request, 'cars/statistics.html', {"type": 'stat', "total_price": total_price, "total_quantity": total_quantity,
                                                         "mean_price": mean_price, "mean_age": mean_age, "mode_type": mode_type,
                                                         "profit_type": profit_type, "profit_car": profit_car, "less_profit_car": less_profit_car,
                                                         "month_chart": month_chart, "year_chart": year_chart, "region_chart": cus_reg_chart,
                                                         "car_type_table": car_type_table})

def sales_month_chart():
    monthly_sales = Complete_Order.objects.annotate(
        month=TruncMonth('date_delivery')).values(
        'month', 'order__car__type__name').annotate(
        total_sales=Sum('total_price')).order_by('month', 'order__car__type__name')
    
    sales_data = defaultdict(lambda: defaultdict(float))
    for entry in monthly_sales:
        month = entry['month'].strftime('%Y-%m')  
        car_type = entry['order__car__type__name']
        total_sales = entry['total_sales']
        sales_data[month][car_type] += total_sales
    
    sales_data = {k: dict(v) for k, v in sales_data.items()}

    months = sorted(sales_data.keys())
    car_types = set()
    for sales in sales_data.values():
        car_types.update(sales.keys())
    car_types = sorted(car_types)

    plot_data = {car_type: [sales_data[month].get(car_type, 0) for month in months] for car_type in car_types}

    plt.figure(figsize=(8, 6))
    for car_type, sales in plot_data.items():
        plt.plot(months, sales, label=car_type)

    plt.xlabel('Месяц')
    plt.ylabel('Объем продаж')
    plt.title('Ежемесячный объем продаж товаров каждого вида')
    plt.legend(title='Тип товара')
    plt.xticks(rotation=45)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()

    return image_base64

def yearly_sales_chart():
    yearly_sales = Complete_Order.objects.annotate(
        year=TruncYear('date_delivery')
    ).values(
        'year'
    ).annotate(
        total_sales=Sum('total_price')
    ).order_by('year')

    years = [entry['year'].year for entry in yearly_sales]
    total_sales = [entry['total_sales'] for entry in yearly_sales]

    plt.figure(figsize=(8, 6))
    plt.plot(years, total_sales, marker='o', linestyle='-')
    plt.xlabel('Год')
    plt.ylabel('Общий объем продаж')
    plt.title('Годовой отчет поступлений от продаж')
    plt.grid(True)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()

    return image_base64

def region_chart():
    timezones = Customer.objects.values_list('time_zone', flat=True)
    timezone_counts = {}
    for timezone in timezones:
        if timezone in timezone_counts:
            timezone_counts[timezone] += 1
        else:
            timezone_counts[timezone] = 1
    
    sorted_timezones = sorted(timezone_counts.items(), key=lambda x: x[1], reverse=True)
    
    labels = [timezone[0] for timezone in sorted_timezones]
    counts = [timezone[1] for timezone in sorted_timezones]
    
    plt.figure(figsize=(8, 8))
    plt.pie(counts, labels=labels, autopct='%1.1f%%', startangle=0)
    plt.axis('equal')  
    plt.title('Распределение клиентов по регионам')

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()

    return image_base64

def car_type_pivot_table():
    cars = Car.objects.all()

    data = {
        'Car Name': [car.name for car in cars],
        'Car Type': [car.type.name for car in cars],
        'Price': [car.price for car in cars]
    }
    df = pd.DataFrame(data)

    pivot_table = pd.pivot_table(df, values='Price', index='Car Type', aggfunc='sum')

    pivot_table_html = pivot_table.to_html()

    return pivot_table_html

def contacts(request):
    contacts = Employee.objects.all()
    return render(request, 'cars/contacts.html',{"contacts": contacts})

def privacy_policy(request):
    return render(request, 'cars/privacypolicy.html')

def vacancy(request):
    vacancies = Vacancy.objects.all()
    return render(request, 'cars/vacancy.html', {"vacancies": vacancies})

@login_required
def promocode(request):
    promocodes = Promocode.objects.all()
    return render(request, 'cars/promocodes.html', {"promocodes": promocodes})

def faq(request):
    faqs = FAQ.objects.all()
    return render(request, 'cars/faq.html', {"faqs": faqs})
    
class Reviews(View):
    def post(self,request,*args,**kwargs):
        text = request.POST.get('text')
        rate = request.POST.get('rate')
        if request.POST.get('Add Review'):
            Review.objects.create(text=text, author=request.user, rate=rate, date=timezone.now().date())
            return redirect('/review')
        
        return redirect('/review')

    def get(self,request,*args,**kwargs):
        reviews = Review.objects.all()

        if request.user.is_anonymous: tp_us = 's'
        else:
            if Customer.objects.filter(user=request.user): tp_us = 'c' 
            else: tp_us = 's'

        if tp_us == 'c':
            return render(request, 'cars/reviews.html', {"reviews": reviews, "type": 'c'})
        
        return render(request, 'cars/reviews.html', {"reviews": reviews, "type": 's'})

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"detail": "Successfully logged out."})