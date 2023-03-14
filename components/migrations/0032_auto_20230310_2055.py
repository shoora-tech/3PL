# Generated by Django 3.2.18 on 2023-03-10 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('components', '0031_fuel_local_exchange_rate'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='local_exchange_rate',
            field=models.FloatField(default=1),
        ),
        migrations.AlterField(
            model_name='customer',
            name='price',
            field=models.FloatField(default=0, verbose_name='Price(USD)'),
        ),
    ]
