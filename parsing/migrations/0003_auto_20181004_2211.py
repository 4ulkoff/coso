# Generated by Django 2.1.1 on 2018-10-04 16:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parsing', '0002_auto_20181004_1944'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='code',
            name='distr',
        ),
        migrations.RemoveField(
            model_name='code',
            name='product',
        ),
        migrations.DeleteModel(
            name='Code',
        ),
    ]