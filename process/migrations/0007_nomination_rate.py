# Generated by Django 3.2.16 on 2023-02-25 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0006_auto_20230225_1437'),
    ]

    operations = [
        migrations.AddField(
            model_name='nomination',
            name='rate',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]
