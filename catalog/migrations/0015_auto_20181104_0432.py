# Generated by Django 2.1.1 on 2018-11-03 22:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0014_product'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ('name',), 'verbose_name': 'Категория', 'verbose_name_plural': 'Категории'},
        ),
        migrations.AlterModelOptions(
            name='vendor',
            options={'ordering': ('vendor',), 'verbose_name': 'Вендор', 'verbose_name_plural': 'Вендоры'},
        ),
        migrations.AlterField(
            model_name='category',
            name='img',
            field=models.ImageField(blank=True, help_text='Картинка соответствующая категории', upload_to='', verbose_name='Картинка'),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='img',
            field=models.ImageField(blank=True, help_text='Логотип производителя', upload_to='', verbose_name='Картинка'),
        ),
    ]
