# Generated by Django 3.2.18 on 2023-03-03 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('components', '0023_fuel_exchange_rate'),
    ]

    operations = [
        migrations.AddField(
            model_name='discountmaster',
            name='exchange_rate',
            field=models.FloatField(default=0),
        ),
    ]