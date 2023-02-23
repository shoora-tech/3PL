# Generated by Django 3.2.18 on 2023-02-22 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('components', '0010_auto_20230222_1356'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transporter',
            old_name='account_number',
            new_name='account_number_TZS_account',
        ),
        migrations.RenameField(
            model_name='transporter',
            old_name='bank_name',
            new_name='bank_name_TZS_account',
        ),
        migrations.RenameField(
            model_name='transporter',
            old_name='name_in_bank_tzs_account',
            new_name='bank_name_USD_account',
        ),
        migrations.RenameField(
            model_name='transporter',
            old_name='name_in_bank_usd_account',
            new_name='name_in_bank_TZS_account',
        ),
        migrations.RenameField(
            model_name='transporter',
            old_name='swift_code',
            new_name='swift_code_TZS_account',
        ),
        migrations.AddField(
            model_name='transporter',
            name='account_number_USD_account',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='transporter',
            name='name_in_bank_USD_account',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='transporter',
            name='swift_code_USD_account',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
