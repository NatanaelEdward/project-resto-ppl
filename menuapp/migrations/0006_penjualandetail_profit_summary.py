# Generated by Django 4.2.4 on 2023-10-30 09:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('menuapp', '0005_penjualandetail_faktur'),
    ]

    operations = [
        migrations.AddField(
            model_name='penjualandetail',
            name='profit_summary',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='menuapp.profitsummary'),
        ),
    ]
