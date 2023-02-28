# Generated by Django 3.2.18 on 2023-02-28 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('components', '0020_alter_currencyexchange_exchange_rate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='cost',
            field=models.FloatField(blank=True, default=0, null=True, verbose_name='Cost (USD)'),
        ),
        migrations.AlterField(
            model_name='product',
            name='tolerance',
            field=models.FloatField(blank=True, default=0, null=True, verbose_name='Tolerance (%)'),
        ),
    ]
