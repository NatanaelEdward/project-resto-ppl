# Generated by Django 4.2.4 on 2023-10-08 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menuapp', '0003_cartitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='penjualandetail',
            name='nomor_nota_penjualan',
            field=models.CharField(max_length=20),
        ),
    ]