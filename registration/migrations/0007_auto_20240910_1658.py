# Generated by Django 3.2 on 2024-09-10 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0006_alter_profile_cid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='client_type',
            field=models.IntegerField(choices=[(0, 'Comprador'), (1, 'Productor'), (2, 'Distribuidor')], default=0, help_text='Puede cambiarlo cuando desee en su perfil', verbose_name='Tipo de cliente'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='money_type',
            field=models.IntegerField(choices=[(0, 'USD'), (1, 'CUP'), (2, 'MLC')], default=0, help_text='En cualquier momento puede cambiarla', verbose_name='Tipo de moneda'),
        ),
    ]