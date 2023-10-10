# Generated by Django 4.2.4 on 2023-10-09 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menuapp', '0007_alter_cartitem_qty'),
    ]

    operations = [
        migrations.CreateModel(
            name='PenjualanFaktur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kode_penjualan_faktur', models.CharField(max_length=20, unique=True)),
                ('nomor_nota_penjualan', models.CharField(max_length=20)),
                ('nomor_meja', models.CharField(max_length=10)),
                ('cara_pembayaran', models.CharField(max_length=50)),
                ('status_lunas', models.BooleanField(default=False)),
                ('jenis_pembayaran', models.CharField(max_length=50)),
                ('tanggal_penjualan', models.DateTimeField(auto_now_add=True)),
                ('total_penjualan', models.DecimalField(decimal_places=2, max_digits=10)),
                ('pembayaran', models.DecimalField(decimal_places=2, max_digits=10)),
                ('kembalian', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
    ]