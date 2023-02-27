# Generated by Django 3.2.18 on 2023-02-27 17:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0020_auto_20230227_1122'),
    ]

    operations = [
        migrations.AddField(
            model_name='summary',
            name='fullfillment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fullfillment_summary', to='process.fullfillment'),
        ),
        migrations.AddField(
            model_name='summary',
            name='nomination',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='nomination_summary', to='process.nomination'),
        ),
        migrations.AddField(
            model_name='summary',
            name='transit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transit_summary', to='process.transit'),
        ),
    ]
