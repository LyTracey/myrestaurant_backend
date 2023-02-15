from rest_framework import serializers
from . import models
import logging
import json
from .utils import list_to_JSON

logger = logging.getLogger(__name__)

class InventorySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Inventory
        exclude = ["slug"]


class MenuInventorySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.MenuInventory
        fields = "__all__"


class MenuSerializer(serializers.ModelSerializer):

    ingredients = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=models.Inventory.objects.all().order_by("ingredient"),
        style={'base_template': 'checkbox_multiple.html'}
    )

    units = serializers.JSONField(
        write_only=True,
        initial=models.Inventory.objects.all().order_by("ingredient"),
        style={'template': 'myrestaurant_app/number_multiple.html'}
    )

    class Meta:
        model = models.Menu
        exclude = ["ingredients_cost", "slug"]
        lookup_field = "slug"

    def to_internal_value(self, data):
        new_data = data.copy()
        units_keys = new_data.pop('units_keys')
        units_data = new_data.pop('units')
        new_data["units"] = list_to_JSON(units_keys, units_data)
        logger.debug(new_data)
        return super().to_internal_value(new_data)

    def create(self, validated_data, **kwargs):
        logger.debug(validated_data)
        ingredients = validated_data.pop('ingredients')
        units = validated_data.pop('units')
        
        # Calculate ingredients_cost
        ingredients_cost = sum([item.unit_price*units[str(item)] for item in ingredients])

        # Create menu model instance
        menu_item = models.Menu.objects.create(**validated_data, ingredients_cost=ingredients_cost)

        # Create menu_inventory data instances
        for item in ingredients:
            obj = models.MenuInventory.objects.create(
                menu_id=menu_item,
                inventory_id=item,
                units=units[str(item)]
            )

        return menu_item


class OrderSerializer(serializers.ModelSerializer):
    menu_items = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=models.Menu.objects.all().order_by("title"),
        style={'base_template': 'checkbox_multiple.html'}
    )

    quantity = serializers.JSONField(
        write_only=True,
        initial=models.Menu.objects.values_list("title", flat=True).order_by("title"),
        style={'template': 'myrestaurant_app/number_multiple.html'}
    )

    class Meta:
        model = models.Order
        fields = "__all__"

    def to_internal_value(self, data):
        new_data = data.copy()
        quantity_keys = new_data.pop('quantity_keys')
        quantity_data = new_data.pop('quantity')
        new_data["quantity"] = list_to_JSON(quantity_keys, quantity_data)
        return super().to_internal_value(new_data)

    def create(self, validated_data, **kwargs):
        menu_items = validated_data.pop('menu_items')
        quantity = validated_data.pop('quantity')

        # Create Order model instance
        order = models.Order.objects.create(**validated_data)

        # Create order_menu data
        for item in menu_items:
            obj = models.OrderMenu.objects.create(
                order_id=order,
                menu_id=item,
                quantity=quantity[str(item)]
            )
       
        return order



class DashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Dashboard
        fields = ["order_statistics", "menu_statistics", "inventory_statistics"]
