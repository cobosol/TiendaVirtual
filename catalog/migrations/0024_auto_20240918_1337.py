# Generated by Django 3.2 on 2024-09-18 13:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0023_product_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='price_usd',
            new_name='price_base',
        ),
        migrations.RemoveField(
            model_name='product',
            name='min_whole',
        ),
        migrations.RemoveField(
            model_name='product',
            name='priceW_cup',
        ),
        migrations.RemoveField(
            model_name='product',
            name='priceW_mlc',
        ),
        migrations.RemoveField(
            model_name='product',
            name='priceW_usd',
        ),
        migrations.RemoveField(
            model_name='product',
            name='price_cup',
        ),
        migrations.RemoveField(
            model_name='product',
            name='price_mlc',
        ),
    ]
