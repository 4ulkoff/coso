# Generated by Django 2.1.3 on 2019-01-13 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parsing', '0023_distrcurrency'),
    ]

    operations = [
        migrations.CreateModel(
            name='Forex',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ask', models.FloatField()),
                ('bid', models.FloatField()),
                ('time', models.DateTimeField()),
            ],
        ),
    ]
