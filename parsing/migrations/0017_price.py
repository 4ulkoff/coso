# Generated by Django 2.1.1 on 2018-11-05 22:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0015_auto_20181104_0432'),
        ('parsing', '0016_auto_20181106_0424'),
    ]

    operations = [
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.SmallIntegerField(choices=[(0, 'Не активно'), (1, 'Активно'), (2, 'Заблокировано')], db_index=True, default=1, help_text='Тип', verbose_name='Тип')),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Оптовая цена')),
                ('retail', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Розничная цена')),
                ('date', models.DateTimeField(verbose_name='Дата')),
                ('code', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='parsing.Code', verbose_name='Код дистрибьютора')),
                ('distr', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='parsing.Distr', verbose_name='Дистрибьютор')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.Product', verbose_name='Продукт')),
            ],
            options={
                'verbose_name': 'Цена',
                'verbose_name_plural': 'Цены',
            },
        ),
    ]
