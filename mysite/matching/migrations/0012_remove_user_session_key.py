# Generated by Django 2.0.4 on 2018-04-23 12:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('matching', '0011_auto_20180423_2039'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='session_key',
        ),
    ]
