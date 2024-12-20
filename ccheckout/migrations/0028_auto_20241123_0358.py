# Generated by Django 3.2 on 2024-11-23 03:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0004_price_min_delivery_free'),
        ('catalog', '0027_product_has_discount'),
        ('ccheckout', '0027_remove_order_delivery_address_1'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivery_apto',
            field=models.CharField(blank=True, default=' ', max_length=100, null=True, verbose_name='Número/Apartamento'),
        ),
        migrations.AlterField(
            model_name='order',
            name='delivery_between',
            field=models.CharField(blank=True, default=' ', max_length=100, null=True, verbose_name='Entre calles'),
        ),
        migrations.AlterField(
            model_name='order',
            name='delivery_street',
            field=models.CharField(blank=True, default=' ', max_length=100, null=True, verbose_name='Calle'),
        ),
        migrations.AlterField(
            model_name='order',
            name='delivery_substate',
            field=models.IntegerField(choices=[(0, 'Guanabacoa'), (1, 'La Habana del Este'), (2, 'Cerro'), (3, 'Cotorro'), (4, 'Diez de Octubre'), (5, 'La Habana Vieja'), (6, 'Centro Habana'), (7, 'San Miguel del Padrón'), (8, 'Boyeros'), (9, 'Marianao'), (10, 'La Lisa'), (11, 'Plaza de la Revolución'), (12, 'Playa'), (13, 'Regla'), (14, 'Arroyo Naranjo')], default=0, verbose_name='Municipio'),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_city',
            field=models.CharField(help_text='Ciudad del banco de la tarjeta', max_length=20, verbose_name='Ciudad del banco'),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_name',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Nombre del titular de la tarjeta'),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_phone',
            field=models.CharField(max_length=20, verbose_name='Teléfono del titular'),
        ),
        migrations.AlterField(
            model_name='order',
            name='price',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='utils.price', verbose_name='Valores para el cálculo del Precio de la compra'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='catalog.product', verbose_name='Producto'),
        ),
    ]
