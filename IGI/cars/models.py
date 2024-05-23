from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
User = get_user_model()

class CarType(models.Model):
    name = models.CharField(max_length=20, help_text='Type (Automobile, Electromobile, Bike)')

    def __str__(self):
        return self.name


class Manufacturer(models.Model):
    name = models.CharField(max_length=20, help_text='Manufacturer (BMW, Toyota, Ferrari etc.)')

    def __str__(self):
        return self.name


class Car(models.Model):
    name = models.CharField(max_length=30, help_text= 'Car name')
    characteristics = models.CharField(max_length=2000, help_text= 'Information/characteristics')
    price = models.FloatField(help_text='Price')
    photo = models.ImageField(default='Nones')
    manufacturer = models.ForeignKey(Manufacturer, related_name='manufacturers', on_delete=models.CASCADE)
    type = models.ForeignKey(CarType, related_name='cars', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=30, help_text='Phone number', default='Not specified')
    birth = models.DateField(null=True)
    time_zone = models.CharField(max_length=50, default='UTC', help_text='Time zone')

    def __str__(self):
        return self.user.get_username()

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    position = models.CharField(max_length=100, help_text='Position in company', default='Not specified')
    photo = models.ImageField(default="Nones")
    phone_number = models.CharField(max_length=30, help_text='Phone number', default='Not specified')
    birth = models.DateField(null=True)
    time_zone = models.CharField(max_length=50, default='UTC', help_text='Time zone')

    def __str__(self):
        return self.user.get_username()   

class Order(models.Model):
    date_order = models.DateField(help_text='Date of order')
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    quantity = models.IntegerField(help_text='Quantity')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    is_complete = models.BooleanField(default=False)
    
    def __str__(self):
        return self.car.name

class Complete_Order(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, default=None)
    total_price = models.IntegerField(help_text='Total price of order')
    date_delivery = models.DateField(help_text='Date of delivery')
    
    def __str__(self):
        return self.order.car.name

class News(models.Model):
    text = models.TextField(max_length=2000)
    title = models.CharField(max_length=100)
    author = models.ForeignKey(User, related_name="news", on_delete=models.CASCADE)
    date = models.DateField()
    photo = models.ImageField(default="Nones", blank=True)

class Review(models.Model):
    text = models.TextField(max_length=2000)
    author = models.ForeignKey(User, related_name="reviews", on_delete=models.CASCADE)
    date = models.DateField()
    rate = models.IntegerField(validators=[ MinValueValidator(1), MaxValueValidator(5) ])

class FAQ(models.Model):
    question=models.CharField(max_length=200)
    answer = models.CharField(max_length=1000)
    date = models.DateField()

class CompanyInfo(models.Model):
    name = models.CharField(max_length=30, help_text= 'Company name')
    description = models.CharField(max_length=2000, help_text='Company description')

class Vacancy(models.Model):
    name = models.CharField(max_length=30, help_text= 'Vacancy name')
    title = models.CharField(max_length=200, help_text= 'Vacancy title')
    description = models.CharField(max_length=2000, help_text='Vacancy description')

    def __str__(self):
        return self.name
    
class Promocode(models.Model):
    name = models.CharField(max_length=30, help_text= 'Promocode name')
    description = models.CharField(max_length=2000, help_text='Promocode description')
    code = models.CharField(max_length=10, help_text='Promocode code')
    discount = models.IntegerField(help_text='Discount value in %', default=0)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.name

