# Generated by Django 4.1.5 on 2023-05-01 12:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myrestaurant_app', '0011_menu_available_quantity'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['-ordered_at']},
        ),
    ]
