# Generated by Django 3.2 on 2024-05-08 18:29

from django.db import migrations
import django_ckeditor_5.fields


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0013_auto_20240506_1425'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='presentation',
            field=django_ckeditor_5.fields.CKEditor5Field(verbose_name='Text'),
        ),
    ]