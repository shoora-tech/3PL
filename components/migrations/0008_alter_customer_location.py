# Generated by Django 3.2.18 on 2023-02-22 04:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('components', '0007_auto_20230221_2037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='location',
            field=models.ManyToManyField(blank=True, related_name='locations', to='components.Location'),
        ),
    ]