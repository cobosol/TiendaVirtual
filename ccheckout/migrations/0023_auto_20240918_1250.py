# Generated by Django 3.2 on 2024-09-18 12:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0001_initial'),
        ('ccheckout', '0022_order_currency'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='price',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='utils.price', verbose_name='Valores para e cálculo del Precio de la compra'),
        ),
        migrations.AlterField(
            model_name='order',
            name='transaction_id',
            field=models.CharField(max_length=20, verbose_name='Nro. Transacción'),
        ),
    ]
