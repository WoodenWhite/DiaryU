# Generated by Django 2.0.4 on 2018-04-29 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matching', '0016_pairing_pair_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='room',
            field=models.CharField(max_length=10000, null=True),
        ),
    ]
