# Generated by Django 2.1.1 on 2018-11-18 03:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0018_auto_20181111_0730'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='img',
            field=models.ImageField(blank=True, help_text='Картинка спродукта', null=True, upload_to='', verbose_name='Картинка'),
        ),
    ]
