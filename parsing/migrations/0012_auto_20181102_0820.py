# Generated by Django 2.1.1 on 2018-11-02 02:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parsing', '0011_auto_20181102_0809'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='distrcategory',
            name='category',
        ),
        migrations.RemoveField(
            model_name='distrcategory',
            name='distr',
        ),
        migrations.DeleteModel(
            name='DistrCategory',
        ),
    ]
