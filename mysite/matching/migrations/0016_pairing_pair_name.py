# Generated by Django 2.0.4 on 2018-04-29 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matching', '0015_auto_20180429_1739'),
    ]

    operations = [
        migrations.AddField(
            model_name='pairing',
            name='pair_name',
            field=models.CharField(max_length=10000, null=True),
        ),
    ]
