# Generated by Django 4.1.5 on 2023-04-15 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myrestaurant_app', '0005_alter_menuinventory_inventory_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='total_cost',
            field=models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=5),
        ),
    ]
