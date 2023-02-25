# Generated by Django 3.2.16 on 2023-02-25 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('components', '0009_auto_20230225_1646'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sellables',
            name='price',
        ),
        migrations.AlterField(
            model_name='manufacturer',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='product',
            name='cost',
            field=models.FloatField(blank=True, null=True, verbose_name='Cost (USD)'),
        ),
        migrations.AlterField(
            model_name='product',
            name='tolerance',
            field=models.FloatField(blank=True, null=True, verbose_name='Tolerance (%)'),
        ),
    ]
