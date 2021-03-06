# Generated by Django 2.1.1 on 2018-11-03 22:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('parsing', '0013_distrcategory'),
    ]

    operations = [
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.SmallIntegerField(choices=[(0, 'Не активно'), (1, 'Активно'), (2, 'Заблокировано')], db_index=True, default=1, help_text='Тип', verbose_name='Тип')),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, verbose_name='Оптовая цена')),
                ('retail', models.DecimalField(blank=True, decimal_places=2, max_digits=10, verbose_name='Розничная цена')),
                ('date', models.DateTimeField(verbose_name='Дата')),
                ('code', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='parsing.Code', verbose_name='Код дистрибьютора')),
            ],
            options={
                'verbose_name': 'Цена',
                'verbose_name_plural': 'Цены',
            },
        ),
        migrations.AlterModelOptions(
            name='exceptcode',
            options={'verbose_name': 'Исключённый код', 'verbose_name_plural': 'Исключённые коды'},
        ),
        migrations.AlterField(
            model_name='distr',
            name='img',
            field=models.ImageField(blank=True, help_text='Логотип дистрибьютора (Желательно SVG)', upload_to='', verbose_name='Лого'),
        ),
        migrations.AlterField(
            model_name='distrcategory',
            name='type',
            field=models.SmallIntegerField(choices=[(0, 'Неактивна'), (1, 'Активная'), (2, 'Заблокированна'), (3, 'Новая')], db_index=True, default=2, help_text='Тип', verbose_name='Тип'),
        ),
        migrations.AddField(
            model_name='price',
            name='distr',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='parsing.Distr', verbose_name='Дистрибьютор'),
        ),
        migrations.AddField(
            model_name='price',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.Product', verbose_name='Продукт'),
        ),
    ]
