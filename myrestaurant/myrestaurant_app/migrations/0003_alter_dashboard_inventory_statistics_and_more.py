# Generated by Django 4.1.5 on 2023-02-06 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myrestaurant_app', '0002_alter_dashboard_inventory_statistics_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dashboard',
            name='inventory_statistics',
            field=models.JSONField(default=dict, null=True),
        ),
        migrations.AlterField(
            model_name='dashboard',
            name='menu_statistics',
            field=models.JSONField(default=dict, null=True),
        ),
        migrations.AlterField(
            model_name='dashboard',
            name='order_statistics',
            field=models.JSONField(default=dict, null=True),
        ),
    ]
