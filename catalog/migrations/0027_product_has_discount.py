# Generated by Django 3.2 on 2024-10-25 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0026_auto_20241024_1504'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='has_discount',
            field=models.BooleanField(default=False, verbose_name='Descuento por cantidad'),
        ),
    ]