# Generated by Django 5.0.6 on 2024-05-19 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0010_vacancy'),
    ]

    operations = [
        migrations.CreateModel(
            name='Promocode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Promocode name', max_length=30)),
                ('description', models.CharField(help_text='Promocode description', max_length=2000)),
                ('code', models.CharField(help_text='Promocode code', max_length=10)),
            ],
        ),
    ]
