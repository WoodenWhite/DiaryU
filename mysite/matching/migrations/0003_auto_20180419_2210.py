# Generated by Django 2.0.4 on 2018-04-19 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matching', '0002_auto_20180419_2126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diary',
            name='pub_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='session_key',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='sex',
            field=models.IntegerField(choices=[(0, '0')], default=0, null=True),
        ),
    ]