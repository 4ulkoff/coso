# Generated by Django 2.1.1 on 2018-11-18 12:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parsing', '0020_auto_20181118_0943'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='currency',
            name='category',
        ),
        migrations.RemoveField(
            model_name='currency',
            name='distr',
        ),
        migrations.DeleteModel(
            name='Currency',
        ),
    ]
