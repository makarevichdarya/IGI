# Generated by Django 5.0.6 on 2024-05-23 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0020_promocode_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='promocode',
            name='discount',
            field=models.IntegerField(default=0, help_text='Discount value in %'),
        ),
    ]
