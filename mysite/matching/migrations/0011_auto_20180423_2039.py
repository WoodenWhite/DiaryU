# Generated by Django 2.0.4 on 2018-04-23 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matching', '0010_auto_20180423_2039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.IntegerField(choices=[(0, '0'), (1, '1'), (2, '2')], default=0, null=True),
        ),
    ]
