# Generated by Django 3.2 on 2024-10-24 21:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ccheckout', '0026_auto_20241024_2059'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='delivery_address_1',
        ),
    ]
