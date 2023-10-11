# Generated by Django 4.2.4 on 2023-10-10 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menuapp', '0008_penjualanfaktur'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataMeja',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nomor_meja', models.CharField(max_length=10, unique=True)),
                ('status_aktif_meja', models.BooleanField(default=True)),
                ('keterangan_meja', models.TextField()),
                ('kapasitas_meja', models.PositiveIntegerField()),
                ('status_terpakai', models.BooleanField(default=False)),
            ],
        ),
    ]