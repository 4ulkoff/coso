# Generated by Django 2.1.1 on 2018-10-04 13:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0011_auto_20181002_1938'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='code',
        ),
        migrations.RemoveField(
            model_name='product',
            name='set',
        ),
    ]