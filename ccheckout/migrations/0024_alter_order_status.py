# Generated by Django 3.2 on 2024-09-27 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ccheckout', '0023_auto_20240918_1250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.IntegerField(choices=[(0, 'Solicitada'), (1, 'Procesada'), (2, 'Pagada'), (3, 'Transportando'), (4, 'Cancelada'), (5, 'Entregada'), (6, 'Devuelta'), (7, 'Confirmada')], default=0, verbose_name='Estado'),
        ),
    ]
