# Generated by Django 4.1.5 on 2023-05-09 09:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='myuser',
            old_name='email',
            new_name='username',
        ),
    ]
