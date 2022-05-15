# Generated by Django 4.0.3 on 2022-05-15 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0051_alter_user_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='employe',
            name='date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='employe',
            name='country',
            field=models.CharField(blank=True, choices=[('Tashkent', 'Tashkent'), ('Samarkand', 'Samarkand'), ('Andijan', 'Andijan'), ('Nukus', 'Nukus'), ('Ferghana', 'Ferghana'), ('Bukhoro', 'Bukhara'), ('Namangan', 'Namangan'), ('Urganch', 'Urganch'), ('Qarshi', 'Qarshi'), ('Jizzakh', 'Jizzakh'), ('Termiz', 'Termiz'), ('Navoiy', 'Navoiy'), ('Sirdaryo', 'Sirdaryo')], max_length=120, null=True),
        ),
    ]
