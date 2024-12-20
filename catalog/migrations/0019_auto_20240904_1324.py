# Generated by Django 3.2 on 2024-09-04 13:24

import catalog.models
import catalog.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0018_auto_20240822_1953'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='count',
            field=models.IntegerField(default=0, help_text='Cantidad del producto en inventarios', verbose_name='Cantidad'),
        ),
        migrations.AlterField(
            model_name='product',
            name='meta_description',
            field=models.CharField(help_text='Contenido clave para el SEO', max_length=255),
        ),
        migrations.AlterField(
            model_name='product',
            name='meta_keywords',
            field=models.CharField(help_text='Palabras clave para el SEO', max_length=255),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(help_text='Nombre único para cada tipo de producto.', max_length=255, unique=True, verbose_name='Nombre único'),
        ),
        migrations.AlterField(
            model_name='product',
            name='prod_datasheet',
            field=models.FileField(blank=True, null=True, upload_to=catalog.models.generate_path, validators=[catalog.validators.valid_extension], verbose_name='Ficha técnica'),
        ),
        migrations.AlterField(
            model_name='product',
            name='reserved',
            field=models.IntegerField(default=0, help_text='Cantidad reservados para comprar', verbose_name='Reservados'),
        ),
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(default='URL', help_text='Valor único para URL, se crea automático', max_length=255, unique=True, verbose_name='Nombre para URL'),
        ),
    ]
