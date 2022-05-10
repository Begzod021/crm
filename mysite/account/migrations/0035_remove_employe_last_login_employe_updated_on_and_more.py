# Generated by Django 4.0.3 on 2022-05-10 19:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0034_user_is_online'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employe',
            name='last_login',
        ),
        migrations.AddField(
            model_name='employe',
            name='updated_on',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='employe',
            name='user1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user1_name', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='employe',
            name='user2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user2_name', to=settings.AUTH_USER_MODEL),
        ),
    ]
