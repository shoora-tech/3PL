# Generated by Django 3.2.18 on 2023-03-10 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0035_nomination_local_exchange_rate'),
    ]

    operations = [
        migrations.AddField(
            model_name='advancefuel',
            name='local_currency_discount',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='advancefuel',
            name='local_net_amount',
            field=models.FloatField(default=0),
        ),
    ]
