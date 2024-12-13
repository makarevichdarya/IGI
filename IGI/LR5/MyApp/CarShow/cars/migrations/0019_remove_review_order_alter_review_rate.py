# Generated by Django 5.0.6 on 2024-05-21 20:45

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0018_complete_order_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='order',
        ),
        migrations.AlterField(
            model_name='review',
            name='rate',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)]),
        ),
    ]