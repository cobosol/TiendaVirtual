# Generated by Django 3.2 on 2024-05-04 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ccheckout', '0009_auto_20240503_1828'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivery_ci',
            field=models.CharField(blank=True, max_length=25, null=True, verbose_name='Número de identidad'),
        ),
    ]