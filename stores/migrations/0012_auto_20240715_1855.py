# Generated by Django 3.2 on 2024-07-15 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0011_product_sales_product_store'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product_sales',
            name='product_store',
        ),
        migrations.AddField(
            model_name='product_sales',
            name='products_store',
            field=models.CharField(default='nombre', help_text='Nombre único para cada tipo de producto en cada almacén.', max_length=255, verbose_name='Nombre único'),
        ),
    ]
