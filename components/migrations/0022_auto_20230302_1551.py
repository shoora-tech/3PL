# Generated by Django 3.2.18 on 2023-03-02 10:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('components', '0021_auto_20230228_1044'),
    ]

    operations = [
        migrations.AddField(
            model_name='discountmaster',
            name='currency',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='components.currency'),
        ),
        migrations.AddField(
            model_name='fuel',
            name='currency',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='components.currency'),
        ),
    ]
