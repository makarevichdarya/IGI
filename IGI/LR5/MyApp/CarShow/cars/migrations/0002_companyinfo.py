# Generated by Django 5.0.6 on 2024-05-18 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Company name', max_length=30)),
                ('description', models.CharField(help_text='Company description', max_length=2000)),
            ],
        ),
    ]