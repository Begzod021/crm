# Generated by Django 4.0.3 on 2022-05-11 21:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0045_user_remember_me'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='remember_me',
        ),
    ]
