# Generated by Django 5.0.6 on 2024-05-19 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0007_customer_birth_employee_birth'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='time_zone',
            field=models.CharField(default='UTC', help_text='Time zone', max_length=50),
        ),
    ]
