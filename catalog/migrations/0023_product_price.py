# Generated by Django 3.2 on 2024-09-18 12:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0001_initial'),
        ('catalog', '0022_auto_20240912_1322'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='price',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='utils.price', verbose_name='Precios del producto'),
        ),
    ]
