# Generated by Django 3.2 on 2024-03-24 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0008_store_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='name',
            field=models.CharField(max_length=255, unique=True, verbose_name='Nombre de almacén'),
        ),
        migrations.AlterField(
            model_name='store',
            name='slug',
            field=models.SlugField(blank=True, default=models.CharField(max_length=255, unique=True, verbose_name='Nombre de almacén'), help_text='Valor único de cada tipo de entrega, creado a partir del nombre.', null=True, unique=True, verbose_name='código para URL'),
        ),
    ]
