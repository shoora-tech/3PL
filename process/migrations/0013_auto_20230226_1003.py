# Generated by Django 3.2.16 on 2023-02-26 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0012_nomination_sales_approved'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nomination',
            name='product_quantity',
        ),
        migrations.AddField(
            model_name='nomination',
            name='tanker_capacity',
            field=models.FloatField(default=0),
        ),
    ]