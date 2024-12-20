# Generated by Django 3.2 on 2024-05-06 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0012_auto_20240315_1634'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='presentation',
            field=models.CharField(default='', help_text='Presentación (con unidad de medida).', max_length=50, verbose_name='Presentación'),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(help_text='Valor único de cada producto creado a partir del nombre', unique=True, verbose_name='Código URL'),
        ),
    ]
