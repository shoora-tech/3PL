# Generated by Django 3.2.16 on 2023-02-25 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0007_nomination_rate'),
    ]

    operations = [
        migrations.AddField(
            model_name='transit',
            name='invoice_value',
            field=models.FloatField(default=0),
        ),
    ]
