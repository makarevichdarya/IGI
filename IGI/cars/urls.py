from django.urls import path, re_path, include
from . import views
from django.contrib.auth.views import LogoutView
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register(r'customers', views.CustomerViewSet)

urlpatterns = [
    path('', views.index, name='index'),
    path('news/', views.news),
    path('about/', views.about, name='about'),
    path('registry/', views.Registry.as_view(), name='registry'),
    path('login/', views.Login.as_view()),
    path('contacts/', views.contacts),
    path('privacypolicy/', views.privacy_policy),
    path('vacancy/', views.vacancy),
    path('promocode/', views.promocode),
    path('faq/', views.faq),
    path('cart/', views.Cart.as_view()),
    path('cars/', views.Cars.as_view()),
    re_path(r'^car/(?P<car_id>\d+)/$', views.car_detail, name='car_detail'),
    path('logout/', LogoutView.as_view(next_page='/'), name="logout"),
    path('profile/', views.Profile.as_view()),
    path('review/', views.Reviews.as_view()),
    path('statistics/', views.Statistics.as_view()),
    path('api/', include(router.urls)),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('api/logout/', LogoutView.as_view(), name='api_logout'),
]