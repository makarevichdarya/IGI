from django.contrib import admin
from .models import CarType, Manufacturer, Car, Employee, Order, News, Review, FAQ, CompanyInfo, Customer, Vacancy, Promocode, Complete_Order
from .models import Order, Complete_Order
# Register your models here.
admin.site.register(CarType)

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display=('name', 'type', 'price')
    list_filter=('manufacturer', 'type')
class CarInline(admin.TabularInline):
    model = Car

@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    inlines = [CarInline]
    
admin.site.register(Employee)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(News)
admin.site.register(Review)
admin.site.register(FAQ)
admin.site.register(CompanyInfo)
admin.site.register(Vacancy)
admin.site.register(Promocode)
admin.site.register(Complete_Order)


