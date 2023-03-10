# Generated by Django 3.2.18 on 2023-02-22 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
        ('components', '0008_alter_customer_location'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TransporterOrganizationFuel',
            new_name='DiscountMaster',
        ),
        migrations.AddField(
            model_name='transporter',
            name='account_number',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='transporter',
            name='bank_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='transporter',
            name='name_in_bank_tzs_account',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='transporter',
            name='name_in_bank_usd_account',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='transporter',
            name='swift_code',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
