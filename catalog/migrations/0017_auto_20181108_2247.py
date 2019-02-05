# Generated by Django 2.1.1 on 2018-11-08 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0016_auto_20181108_2219'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ('title',), 'verbose_name': 'Продукт', 'verbose_name_plural': 'Продукты'},
        ),
        migrations.AlterField(
            model_name='product',
            name='number',
            field=models.IntegerField(help_text='Уникальный код товара', unique=True, verbose_name='Нумерация'),
        ),
    ]
