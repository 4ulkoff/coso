# Generated by Django 2.1.1 on 2018-10-04 16:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0012_auto_20181004_1943'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='category',
        ),
        migrations.RemoveField(
            model_name='product',
            name='vendor',
        ),
        migrations.DeleteModel(
            name='Product',
        ),
    ]
