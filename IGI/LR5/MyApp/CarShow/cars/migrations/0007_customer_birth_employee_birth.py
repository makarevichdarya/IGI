# Generated by Django 5.0.6 on 2024-05-18 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0006_remove_customer_firstname_remove_customer_lastname_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='birth',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='birth',
            field=models.DateField(null=True),
        ),
    ]
