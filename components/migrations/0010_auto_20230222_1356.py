# Generated by Django 3.2.18 on 2023-02-22 13:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
        ('components', '0009_auto_20230222_0525'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='DiscountMaster',
            new_name='TransporterOrganizationFuel',
        ),
        migrations.AlterModelOptions(
            name='transporterorganizationfuel',
            options={'verbose_name_plural': 'Discount Master'},
        ),
    ]
