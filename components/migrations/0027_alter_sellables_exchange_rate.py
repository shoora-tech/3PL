# Generated by Django 3.2.18 on 2023-03-03 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('components', '0026_sellables_exchange_rate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sellables',
            name='exchange_rate',
            field=models.FloatField(default=1),
        ),
    ]
