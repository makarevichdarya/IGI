# Generated by Django 5.0.6 on 2024-05-20 20:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0014_alter_order_options_order_deleted_at'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={},
        ),
        migrations.RemoveField(
            model_name='order',
            name='deleted_at',
        ),
    ]
