# Generated by Django 2.1.1 on 2018-11-02 01:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parsing', '0009_auto_20181102_0723'),
    ]

    operations = [
        migrations.RenameField(
            model_name='distrcategory',
            old_name='category',
            new_name='category_id',
        ),
    ]
