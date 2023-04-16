from rest_framework import serializers
from .models import Inventory, Menu, Order, MenuInventory, OrderMenu
import logging
from .scripts.myrestaurant_utils import create_update_menu, create_update_order
from decimal import Decimal
import json
from collections import OrderedDict

logger = logging.getLogger(__name__)

class InventorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Inventory
        exclude = ["slug"]


class MenuInventorySerializer(serializers.ModelSerializer):

    class Meta:
        model = MenuInventory
        fields = ["units"]


class OrderMenuSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderMenu
        fields = "__all__"


class MenuInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuInventory
        fields = ["units"]


class MenuSerializer(serializers.ModelSerializer):

    ingredients = serializers.PrimaryKeyRelatedField(
        queryset=Inventory.objects.all(), 
        many=True
    )

    units = MenuInventorySerializer(many=True, required=False)


    class Meta:
        model = Menu
        fields = ["id", "title", "image", "description", "ingredients", "price", "units"]
        lookup_field = "slug"

    def to_internal_value(self, data):
        logger.debug(data)
        new_data = data.copy()
        units = json.loads(new_data.pop("units")[0])
        internal_representation = super().to_internal_value(new_data)
        internal_representation["units"] = units
        return internal_representation

    def create(self, validated_data, **kwargs):
        return create_update_menu(validated_data, Menu, MenuInventory)

    def update(self, instance, validated_data, **kwargs):
        return create_update_menu(validated_data, Menu, MenuInventory, instance.pk)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        units = {str(item.id): MenuInventory.objects.get(menu_id=instance.id, inventory_id=item.id).units for item in instance.ingredients.all()}
        representation["units"] = units
        return representation
    
class OrderMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderMenu
        fields = ["quantity"]

class OrderSerializer(serializers.ModelSerializer):

    menu_items = serializers.PrimaryKeyRelatedField(
        queryset=Menu.objects.all(),
        many=True
    )

    quantity = OrderMenuSerializer(many=True, required=False)

    class Meta:
        model = Order
        fields = "__all__"
    
    def to_internal_value(self, data):
        new_data = data.copy()
        quantity = json.loads(new_data.pop('quantity')[0])
        internal_representation = super().to_internal_value(new_data)
        internal_representation['quantity'] = quantity
        return internal_representation

    def create(self, validated_data, **kwargs):
        return create_update_order(validated_data, Order, OrderMenu, Inventory)

    def update(self, instance, validated_data):
        return create_update_order(validated_data, Order, OrderMenu, Inventory, Menu, instance.pk)
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        quantity = {str(item.id): OrderMenu.objects.get(order_id=instance.id, menu_id=item.id).quantity for item in instance.menu_items.all()}
        representation["quantity"] = quantity
        return representation

class DashboardSerializer(serializers.Serializer):
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    frequency = serializers.CharField(max_length=3)

