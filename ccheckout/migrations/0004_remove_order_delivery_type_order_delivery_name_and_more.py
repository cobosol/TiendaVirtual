# Generated by Django 4.2.8 on 2024-02-18 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ccheckout', '0003_deliverytype_delete_shippingtype_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='delivery_type',
        ),
        migrations.AddField(
            model_name='order',
            name='delivery_name',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Nombre para la entrega'),
        ),
        migrations.AlterField(
            model_name='order',
            name='billing_state',
            field=models.CharField(max_length=50, verbose_name='Municipio'),
        ),
        migrations.AlterField(
            model_name='order',
            name='delivery_state',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Municipio'),
        ),
    ]