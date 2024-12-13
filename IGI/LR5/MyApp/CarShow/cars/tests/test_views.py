from django.test import TestCase, RequestFactory, Client
from django.contrib.auth.models import User
from django.template.response import TemplateResponse
from django.core.cache import cache
from django.urls import reverse
from unittest.mock import patch
from cars.views import index, news, Registry, Login
from cars.models import News, CompanyInfo, Customer
import datetime
import logging

class IndexViewTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.news = News.objects.create(
            text="Test news",
            title="Test Title",
            author=self.user,
            date=datetime.date(2024,5,5)
        )

    @patch('requests.get')
    def test_index_view(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'quote': {'body': 'Test quote'}}
        
        request = self.factory.get('/')
        response = index(request)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test quote', response.content)
        self.assertIn(b'Test Title', response.content)

    @patch('requests.get')
    def test_index_view_with_cached_quote(self, mock_get):
        cache.set('daily_quote', 'Cached quote', timeout=86400)

        request = self.factory.get('/')
        response = index(request)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Cached quote', response.content)
        self.assertIn(b'Test Title', response.content)

class NewsViewTest(TestCase):
    
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.news1 = News.objects.create(
            text="Test news 1.",
            title="Title 1",
            author=self.user,
            date=datetime.date(2024,5,5)
        )
        self.news2 = News.objects.create(
            text="Test news 2.",
            title="Title 2",
            author=self.user,
            date=datetime.date(2024,5,8)
        )

    def test_news_view(self):
        response = self.client.get('/news/')  
    
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cars/news.html')

class AboutViewTest(TestCase):
    def setUp(self):
        self.company_info = CompanyInfo.objects.create(
            name="Test Company",
            description="Description of the test company"
        )

    def test_about_view(self):
        url = reverse('about')  
        response = self.client.get(url)  

        self.assertEqual(response.status_code, 200)  
        self.assertTemplateUsed(response, 'cars/about.html') 
        self.assertContains(response, self.company_info.name) 
        self.assertContains(response, self.company_info.description)

class RegistryViewTest(TestCase):
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass',
            'first_name': 'Test',
            'last_name': 'User'
        }
        self.registry_url = reverse('registry')  

    def test_successful_registration_redirects_to_home(self):
        
        data = {
            'username': self.user_data['username'],
            'email': self.user_data['email'],
            'password': self.user_data['password'],
            'first_name': self.user_data['first_name'],
            'last_name': self.user_data['last_name'],
            'phone_number': '+375 (29) 000-00-00',
            'birth': datetime.date(1990,1,1),
            'time_zone': 'UTC'
        }
        response = self.client.post(self.registry_url, data)
        
        self.assertFalse(User.objects.filter(username=self.user_data['username']).exists())
        

class LoginViewTest(TestCase):
    def setUp(self):
        self.client = Client() 
        self.login_url = reverse('login')  

    def test_login_view(self):
        user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass')
        customer = Customer.objects.create(user=user, phone_number='123456789', birth='1990-01-01', time_zone='UTC')

        response = self.client.post(self.login_url, {'username': 'testuser', 'password': 'testpass'})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')  

    def test_login_view_invalid_credentials(self):
        response = self.client.post(self.login_url, {'username': 'invaliduser', 'password': 'invalidpass'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Wrong username or password')
        