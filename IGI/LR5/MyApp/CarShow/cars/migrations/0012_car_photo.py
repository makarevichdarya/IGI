# Generated by Django 5.0.6 on 2024-05-19 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0011_promocode'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='photo',
            field=models.ImageField(default='Nones', upload_to=''),
        ),
    ]
