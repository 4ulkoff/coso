# Generated by Django 2.1.3 on 2018-12-02 23:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mrm', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.SmallIntegerField(choices=[(0, 'Не активен'), (1, 'Основной'), (2, 'Дополнительный')], db_index=True, default=1, help_text='Тип контакта', verbose_name='Тип')),
                ('email', models.EmailField(max_length=254, verbose_name='E-mail')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='mrm.Member', verbose_name='Участник')),
            ],
            options={
                'verbose_name': 'E-mail',
            },
        ),
    ]
