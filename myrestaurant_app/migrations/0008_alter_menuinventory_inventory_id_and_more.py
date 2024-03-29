# Generated by Django 4.1.5 on 2023-04-15 14:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myrestaurant_app', '0007_alter_ordermenu_menu_id_alter_ordermenu_order_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuinventory',
            name='inventory_id',
            field=models.ForeignKey(db_column='inventory_id', on_delete=django.db.models.deletion.CASCADE, to='myrestaurant_app.inventory'),
        ),
        migrations.AlterField(
            model_name='menuinventory',
            name='menu_id',
            field=models.ForeignKey(db_column='menu_id', on_delete=django.db.models.deletion.CASCADE, to='myrestaurant_app.menu'),
        ),
        migrations.AlterField(
            model_name='ordermenu',
            name='menu_id',
            field=models.ForeignKey(db_column='menu_id', on_delete=django.db.models.deletion.CASCADE, to='myrestaurant_app.menu'),
        ),
        migrations.AlterField(
            model_name='ordermenu',
            name='order_id',
            field=models.ForeignKey(db_column='order_id', on_delete=django.db.models.deletion.CASCADE, to='myrestaurant_app.order'),
        ),
    ]
