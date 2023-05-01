# Generated by Django 4.1.5 on 2023-04-15 13:45

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myrestaurant_app', '0006_order_total_cost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordermenu',
            name='menu_id',
            field=models.ForeignKey(db_column='menu_id', on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='myrestaurant_app.menu'),
        ),
        migrations.AlterField(
            model_name='ordermenu',
            name='order_id',
            field=models.ForeignKey(db_column='order_id', on_delete=django.db.models.deletion.CASCADE, related_name='quantity', to='myrestaurant_app.order'),
        ),
        migrations.AlterField(
            model_name='ordermenu',
            name='quantity',
            field=models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(0, message='unit is not a positive')]),
        ),
    ]
