from rest_framework import serializers
from . import models
import logging
import json

logger = logging.getLogger(__name__)

class InventorySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Inventory
        fields = ["ingredient", "quantity", "unit_price", "image"]


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
        fields = "__all__"
        lookup_field = "slug"

    def to_internal_value(self, data):
        new_data = data.copy()
        ingredients_data = new_data.pop('ingredient_name')
        units_data = new_data.pop('units')
        new_data['units'] = json.dumps({item[0]: int(item[1]) for item in  zip(ingredients_data, units_data) })
        return super().to_internal_value(new_data)

    def create(self, validated_data, **kwargs):
        units = validated_data.pop('units')
        ingredients = validated_data.pop('ingredients')
        menu_item = models.Menu.objects.create(**validated_data)
        for inventory_item in ingredients:
            models.MenuInventory.objects.create(
                menu_id=menu_item,
                inventory_id=inventory_item,
                units=units[str(inventory_item)]
            )        
        return menu_item


class OrderSerializer(serializers.ModelSerializer):
    menu_items = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=models.Menu.objects.all(),
        style={'base_template': 'checkbox_multiple.html'}
    )

    class Meta:
        model = models.Order
        fields = "__all__"



class DashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Dashboard
        fields = ["order_statistics", "menu_statistics", "inventory_statistics"]
