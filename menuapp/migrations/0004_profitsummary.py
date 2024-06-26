# Generated by Django 4.2.4 on 2023-10-29 10:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('menuapp', '0003_bahanmenu_size'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProfitSummary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pendapatan_bersih', models.DecimalField(decimal_places=2, max_digits=10)),
                ('pendapatan_kotor', models.DecimalField(decimal_places=2, max_digits=10)),
                ('profit', models.DecimalField(decimal_places=2, max_digits=10)),
                ('menu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='menuapp.datamenu')),
            ],
        ),
    ]
