from rest_framework import serializers
from . import models
import logging
from .scripts.myrestaurant_utils import create_update_menu
from decimal import Decimal
import json
from collections import OrderedDict

logger = logging.getLogger(__name__)

class InventorySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Inventory
        exclude = ["slug"]


class MenuInventorySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.MenuInventory
        fields = ["units"]


class OrderMenuSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.OrderMenu
        fields = "__all__"


class MenuInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MenuInventory
        fields = ["units", "inventory_id"]


class MenuSerializer(serializers.ModelSerializer):

    ingredients = serializers.PrimaryKeyRelatedField(
        queryset=models.Inventory.objects.all(), 
        many=True
    )

    units = MenuInventorySerializer(many=True)

    class Meta:
        model = models.Menu
        fields = ["id", "title", "image", "description", "ingredients", "price", "units"]
        lookup_field = "slug"

    def to_internal_value(self, data):
        new_data = data.copy()
        units = json.loads(new_data.pop("units")[0])
        internal_representation = super().to_internal_value(new_data)
        internal_representation["units"] = units
        return internal_representation

    def create(self, validated_data, **kwargs):
        return create_update_menu(validated_data, models.Menu, models.MenuInventory)

    def update(self, instance, validated_data, **kwargs):
        return create_update_menu(validated_data, models.Menu, models.MenuInventory, instance.pk)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        units = {}
        for unit_dict in representation["units"]:
            units[unit_dict["inventory_id"]] = unit_dict["units"]
        representation["units"] = units
        return representation

class OrderSerializer(serializers.ModelSerializer):

    queryset = models.Menu.objects.all().order_by("title")

    menu_items = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=queryset,
        style={'base_template': 'checkbox_multiple.html'}
    )

    quantity = serializers.JSONField(
        write_only=True,
        initial={str(key): 0 for key in queryset},
        style={
            'template': 'myrestaurant_app/number_multiple.html',
            'queryset': queryset
        }
    )

    class Meta:
        model = models.Order
        fields = "__all__"
    
    # def to_internal_value(self, data):
    #     new_data = data.copy()
    #     if new_data.get('keys'):
    #         menu_items = new_data.pop('keys')
    #         quantities = new_data.pop('quantity')
    #         new_data['quantity'] = list_to_JSON(menu_items, quantities)
    #     return super().to_internal_value(new_data)

    def create(self, validated_data, **kwargs):
        menu_items: list[obj] = validated_data.pop('menu_items')
        quantity: dict[int] = validated_data.pop('quantity')

        # Create Order model instance
        order = models.Order.objects.create(**validated_data)

        # Create order_menu data
        for item in menu_items:
            obj = models.OrderMenu.objects.create(
                order_id=order,
                menu_id=item,
                quantity=quantity[str(item)]
            )

        # Update inventory
        for item in menu_items:
            inventory_items = item.menu_inventory.values_list("inventory_id", "units")
            units_used = {k: v*quantity[str(item)] for k, v in inventory_items}
            for id in [k[0] for k in inventory_items]:
                obj = models.Inventory.objects.get(id=id)
                obj.quantity = obj.quantity - units_used[obj.id]
                obj.save()
                
        return order



class DashboardSerializer(serializers.Serializer):
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    frequency = serializers.CharField(max_length=3)

