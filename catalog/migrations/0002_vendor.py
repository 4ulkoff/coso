# Generated by Django 2.1.1 on 2018-10-01 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.SmallIntegerField(choices=[(0, 'Не активно'), (1, 'Активно'), (2, 'Заблокировано')], db_index=True, default=1, help_text='Тип', verbose_name='Тип')),
                ('vendor', models.CharField(help_text='Наименование производителя', max_length=200, verbose_name='Вендор')),
                ('alias', models.CharField(blank=True, help_text='Псевдоним используется для сокращений и русских названий', max_length=200, verbose_name='Псевдоним')),
                ('url', models.URLField(blank=True, help_text='Ссылка на сайт производителя', max_length=300, verbose_name='Ссылка')),
                ('img', models.ImageField(help_text='Картинка соответствующая категории', upload_to='', verbose_name='Картинка')),
            ],
        ),
    ]