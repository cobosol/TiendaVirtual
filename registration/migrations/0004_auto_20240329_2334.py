# Generated by Django 3.2 on 2024-03-30 02:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0003_profile_client_type_alter_profile_bio'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='address',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Dirección oficial'),
        ),
        migrations.AddField(
            model_name='profile',
            name='agency',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Agencia bancaria'),
        ),
        migrations.AddField(
            model_name='profile',
            name='contract',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Número de contrato'),
        ),
        migrations.AddField(
            model_name='profile',
            name='nit',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True, verbose_name='Código NIT'),
        ),
        migrations.AddField(
            model_name='profile',
            name='reeup',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True, verbose_name='Código REEUP'),
        ),
    ]