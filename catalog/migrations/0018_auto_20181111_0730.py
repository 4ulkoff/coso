# Generated by Django 2.1.1 on 2018-11-11 01:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0017_auto_20181108_2247'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ('id',), 'verbose_name': 'Продукт', 'verbose_name_plural': 'Продукты'},
        ),
    ]
