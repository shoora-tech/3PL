# Generated by Django 3.2.18 on 2023-02-21 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('components', '0006_auto_20230221_2019'),
    ]

    operations = [
        migrations.AddField(
            model_name='driver',
            name='driving_license_number',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='driver',
            name='driving_license_validity',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='driver',
            name='passport_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='driver',
            name='passport_validity',
            field=models.DateField(blank=True, null=True),
        ),
    ]