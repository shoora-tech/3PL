# Generated by Django 3.2.18 on 2023-03-03 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0024_auto_20230302_1551'),
    ]

    operations = [
        migrations.AddField(
            model_name='advancecash',
            name='exchange_rate',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='advancecash',
            name='amount',
            field=models.FloatField(default=0),
        ),
    ]