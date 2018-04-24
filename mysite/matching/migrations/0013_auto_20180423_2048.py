# Generated by Django 2.0.4 on 2018-04-23 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matching', '0012_remove_user_session_key'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='openID',
            new_name='openId',
        ),
        migrations.AddField(
            model_name='user',
            name='nickName',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
