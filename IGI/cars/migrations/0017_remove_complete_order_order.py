# Generated by Django 5.0.6 on 2024-05-20 22:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0016_order_is_complete'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='complete_order',
            name='order',
        ),
    ]
