# Generated by Django 4.0.3 on 2022-04-14 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0022_alter_postion_position'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdduserCount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('users', models.PositiveIntegerField()),
            ],
        ),
    ]
