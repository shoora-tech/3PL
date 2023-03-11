# Generated by Django 3.2.18 on 2023-03-10 15:39

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0031_auto_20230310_1510'),
    ]

    operations = [
        migrations.AddField(
            model_name='summary',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='SummaryInLocalCurrency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='UUID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('fullfillment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fullfillment_local_summary', to='process.fullfillment')),
                ('nomination', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='nomination_local_summary', to='process.nomination')),
                ('summary', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='local_summary', to='process.summary')),
                ('transit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transit_local_summary', to='process.transit')),
            ],
            options={
                'verbose_name_plural': 'Summary In Local Currency',
            },
        ),
        migrations.AddField(
            model_name='fullfillment',
            name='summary_in_local_currency',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='local_summary_offload', to='process.summaryinlocalcurrency'),
        ),
        migrations.AddField(
            model_name='nomination',
            name='summary_in_local_currency',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='local_summary_nomination', to='process.summaryinlocalcurrency'),
        ),
        migrations.AddField(
            model_name='summary',
            name='summary_in_local_currency',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='local_summary', to='process.summaryinlocalcurrency'),
        ),
        migrations.AddField(
            model_name='transit',
            name='summary_in_local_currency',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='local_summary_transit', to='process.summaryinlocalcurrency'),
        ),
    ]
