from django.test import TestCase
import datetime
from django.contrib.auth.models import User
from cars.models import CarType, Manufacturer, Car, Customer, Employee, Order, Complete_Order, News

class CarTypeModelTest(TestCase):

    def setUp(self):
        CarType.objects.create(name="Automobile")
        CarType.objects.create(name="Electromobile")
        CarType.objects.create(name="Bike")

    def test_car_type_string_representation(self):
        car_type = CarType.objects.get(name="Automobile")
        self.assertEqual(str(car_type), car_type.name)

    def test_car_type_creation(self):
        automobile = CarType.objects.get(name="Automobile")
        electromobile = CarType.objects.get(name="Electromobile")
        bike = CarType.objects.get(name="Bike")
        
        self.assertEqual(automobile.name, "Automobile")
        self.assertEqual(electromobile.name, "Electromobile")
        self.assertEqual(bike.name, "Bike")

    def test_car_type_max_length(self):
        car_type = CarType.objects.get(name="Automobile")
        max_length = car_type._meta.get_field('name').max_length
        self.assertEqual(max_length, 20)

class ManufacturerModelTest(TestCase):

    def setUp(self):
        Manufacturer.objects.create(name="BMW")
        Manufacturer.objects.create(name="Toyota")
        Manufacturer.objects.create(name="Ferrari")

    def test_manufacturer_string_representation(self):
        manufacturer = Manufacturer.objects.get(name="BMW")
        self.assertEqual(str(manufacturer), manufacturer.name)

    def test_manufacturer_creation(self):
        bmw = Manufacturer.objects.get(name="BMW")
        toyota = Manufacturer.objects.get(name="Toyota")
        ferrari = Manufacturer.objects.get(name="Ferrari")
        
        self.assertEqual(bmw.name, "BMW")
        self.assertEqual(toyota.name, "Toyota")
        self.assertEqual(ferrari.name, "Ferrari")

    def test_manufacturer_max_length(self):
        manufacturer = Manufacturer.objects.get(name="BMW")
        max_length = manufacturer._meta.get_field('name').max_length
        self.assertEqual(max_length, 20)

class CarModelTest(TestCase):

    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(name="BMW")
        self.car_type = CarType.objects.create(name="Automobile")

        self.car = Car.objects.create(
            name="BMW X5",
            characteristics="SUV with luxury features",
            price=50000.00,
            manufacturer=self.manufacturer,
            type=self.car_type
        )

    def test_car_string_representation(self):
        self.assertEqual(str(self.car), self.car.name)

    def test_car_creation(self):
        car = Car.objects.get(name="BMW X5")
        self.assertEqual(car.name, "BMW X5")
        self.assertEqual(car.characteristics, "SUV with luxury features")
        self.assertEqual(car.price, 50000.00)
        self.assertEqual(car.photo.name, "Nones")
        self.assertEqual(car.manufacturer, self.manufacturer)
        self.assertEqual(car.type, self.car_type)

    def test_car_name_max_length(self):
        max_length = self.car._meta.get_field('name').max_length
        self.assertEqual(max_length, 30)

    def test_car_characteristics_max_length(self):
        max_length = self.car._meta.get_field('characteristics').max_length
        self.assertEqual(max_length, 2000)

    def test_car_default_photo(self):
        car = Car.objects.create(
            name="BMW X6",
            characteristics="Another SUV",
            price=60000.00,
            manufacturer=self.manufacturer,
            type=self.car_type
        )
        self.assertEqual(car.photo.name, "Nones")

class CustomerModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.customer = Customer.objects.create(
            user=self.user,
            phone_number="1234567890",
            birth=datetime.date(1990,1,1),
            time_zone="Europe/Moscow"
        )

    def test_customer_string_representation(self):
        self.assertEqual(str(self.customer), self.user.username)

    def test_customer_creation(self):
        customer = Customer.objects.get(user=self.user)
        self.assertEqual(customer.phone_number, "1234567890")
        self.assertEqual(customer.birth, datetime.date(1990,1,1))
        self.assertEqual(customer.time_zone, "Europe/Moscow")

    def test_customer_default_phone_number(self):
        new_user = User.objects.create_user(username="newuser", password="newpass")
        customer = Customer.objects.create(user=new_user)
        self.assertEqual(customer.phone_number, "Not specified")

    def test_customer_default_time_zone(self):
        new_user = User.objects.create_user(username="newuser2", password="newpass2")
        customer = Customer.objects.create(user=new_user)
        self.assertEqual(customer.time_zone, "UTC")

class EmployeeModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.employee = Employee.objects.create(
            user=self.user,
            position="Manager",
            phone_number="1234567890",
            birth=datetime.date(1990,1,1),
            time_zone="Europe/Moscow"
        )

    def test_employee_string_representation(self):
        self.assertEqual(str(self.employee), self.user.username)

    def test_employee_creation(self):
        employee = Employee.objects.get(user=self.user)
        self.assertEqual(employee.position, "Manager")
        self.assertEqual(employee.phone_number, "1234567890")
        self.assertEqual(employee.birth, datetime.date(1990,1,1))
        self.assertEqual(employee.time_zone, "Europe/Moscow")

    def test_employee_default_position(self):
        new_user = User.objects.create_user(username="newuser", password="newpass")
        employee = Employee.objects.create(
            user=new_user
        )
        self.assertEqual(employee.position, "Not specified")

    def test_employee_default_phone_number(self):
        new_user = User.objects.create_user(username="newuser2", password="newpass2")
        employee = Employee.objects.create(
            user=new_user
        )
        self.assertEqual(employee.phone_number, "Not specified")

    def test_employee_default_time_zone(self):
        new_user = User.objects.create_user(username="newuser3", password="newpass3")
        employee = Employee.objects.create(
            user=new_user
        )
        self.assertEqual(employee.time_zone, "UTC")

    def test_employee_default_photo(self):
        new_user = User.objects.create_user(username="newuser4", password="newpass4")
        employee = Employee.objects.create(
            user=new_user
        )
        self.assertEqual(employee.photo.name, "Nones")

class OrderModelTest(TestCase):

    def setUp(self):
        self.client_user = User.objects.create_user(username="client_user", password="testpass")
        self.employee_user = User.objects.create_user(username="employee_user", password="testpass")
        self.car = Car.objects.create(
            name="BMW X5",
            characteristics="SUV with luxury features",
            price=50000.00,
            manufacturer = Manufacturer.objects.create(name="BMW"),
            type=CarType.objects.create(name="Automobile")
        )
        self.employee = Employee.objects.create(
            user=self.employee_user,
            position="Manager",
            phone_number="1234567890",
            birth=datetime.date(1990,1,1),
            time_zone="Europe/Moscow"
        )

    def test_order_creation(self):
        order = Order.objects.create(
            date_order=datetime.date(2024,5,5),
            client=self.client_user,
            car=self.car,
            quantity=2,
            employee=self.employee,
            is_complete=False
        )
        self.assertEqual(order.date_order, datetime.date(2024,5,5))
        self.assertEqual(order.client, self.client_user)
        self.assertEqual(order.car, self.car)
        self.assertEqual(order.quantity, 2)
        self.assertEqual(order.employee, self.employee)
        self.assertFalse(order.is_complete)

    def test_order_string_representation(self):
        order = Order.objects.create(
            date_order=datetime.date(2024,5,5),
            client=self.client_user,
            car=self.car,
            quantity=2,
            employee=self.employee,
            is_complete=False
        )
        expected_string = f"{self.car.name}"
        self.assertEqual(str(order), expected_string)

class CompleteOrderModelTest(TestCase):

    def setUp(self):
        self.client_user = User.objects.create_user(username="client_user", password="testpass")
        self.employee_user = User.objects.create_user(username="employee_user", password="testpass")
        self.car = Car.objects.create(
            name="BMW X5",
            characteristics="SUV with luxury features",
            price=50000.00,
            manufacturer=Manufacturer.objects.create(name="BMW"),
            type=CarType.objects.create(name="Automobile")
        )
        self.employee = Employee.objects.create(
            user=self.employee_user,
            position="Manager",
            phone_number="1234567890",
            birth=datetime.date(1990,1,1),
            time_zone="Europe/Moscow"
        )
        self.order = Order.objects.create(
            date_order=datetime.date(2024,5,5),
            client=self.client_user,
            car=self.car,
            quantity=2,
            employee=self.employee,
            is_complete=False
        )

    def test_complete_order_creation(self):
        complete_order = Complete_Order.objects.create(
            order=self.order,
            total_price=100000,  
            date_delivery=datetime.date(2024,5,10)  
        )
        self.assertEqual(complete_order.order, self.order)
        self.assertEqual(complete_order.total_price, 100000)
        self.assertEqual(complete_order.date_delivery, datetime.date(2024,5,10))

    def test_complete_order_string_representation(self):
        complete_order = Complete_Order.objects.create(
            order=self.order,
            total_price=100000, 
            date_delivery= datetime.date(2024,5,10)
        )
        expected_string = f"{self.order.car.name}"
        self.assertEqual(str(complete_order), expected_string)

class NewsModelTest(TestCase):

    def setUp(self):
        self.author = User.objects.create_user(username="test_author", password="testpass")

    def test_news_creation(self):
        news = News.objects.create(
            text="Text",
            title="Test News",
            author=self.author,
            date=datetime.date(2024,5,5),
            photo=""  
        )
        self.assertEqual(news.text, "Text")
        self.assertEqual(news.title, "Test News")
        self.assertEqual(news.author, self.author)
        self.assertEqual(news.date, datetime.date(2024,5,5))
        self.assertEqual(news.photo, "")

