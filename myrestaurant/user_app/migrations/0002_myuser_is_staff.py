# Generated by Django 4.1.5 on 2023-02-04 23:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
    ]