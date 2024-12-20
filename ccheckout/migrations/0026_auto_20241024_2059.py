# Generated by Django 3.2 on 2024-10-24 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ccheckout', '0025_alter_order_transaction_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivery_apto',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Número/Apartamento'),
        ),
        migrations.AddField(
            model_name='order',
            name='delivery_between',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Entre calles'),
        ),
        migrations.AddField(
            model_name='order',
            name='delivery_street',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Calle'),
        ),
        migrations.AddField(
            model_name='order',
            name='delivery_substate',
            field=models.IntegerField(choices=[(0, 'Guanabacoa'), (1, 'La Habana del Este'), (2, 'Cerro'), (3, 'Cotorro'), (4, 'Diez de Octubre'), (5, 'La Habana Vieja'), (6, 'Centro Habana'), (7, 'San Miguel del Padrón'), (8, 'Boyeros'), (9, 'Marianao'), (10, 'La Lisa'), (11, 'Plaza de la Revolución'), (12, 'Playa'), (13, 'Regla'), (14, 'Arroyo Naranjo')], default=2, verbose_name='Municipio'),
        ),
        migrations.AlterField(
            model_name='order',
            name='delivery_state',
            field=models.CharField(default='La Habana', max_length=50, verbose_name='Provincia'),
        ),
    ]
