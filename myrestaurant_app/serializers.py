from rest_framework import serializers
from .models import Inventory, Menu, Order, MenuInventory, OrderMenu
import logging
from .scripts.serializer_utils import create_update_menu, create_update_order, format_date
import json



logger = logging.getLogger(__name__)

class InventorySerializer(serializers.ModelSerializer):        
    class Meta:
        model = Inventory
        exclude = ["image"]

class InventoryReferenceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Inventory
        fields = ["id", "ingredient"]



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
        exclude = ["ingredients_cost", "image"]
        lookup_field = "slug"

    def to_internal_value(self, data):
        new_data = data.copy()
        units = json.loads(new_data.pop("units")[0])
        internal_representation = super().to_internal_value(new_data)
        internal_representation["units"] = units
        return internal_representation

    def create(self, validated_data, **kwargs):
        return create_update_menu(validated_data)

    def update(self, instance, validated_data, **kwargs):
        return create_update_menu(validated_data, instance.pk)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        units = {str(item.id): MenuInventory.objects.get(menu_id=instance.id, inventory_id=item.id).units for item in instance.ingredients.all()}
        ingredient_names = {ingredient.id: ingredient.ingredient for ingredient in instance.ingredients.all()}
        representation["units"] = units
        representation["ingredients"] = ingredient_names
        return representation
    
class QuantitySerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderMenu
        fields = ["quantity"]

class OrderSerializer(serializers.ModelSerializer):

    menu_items = serializers.PrimaryKeyRelatedField(
        queryset=Menu.objects.all(),
        many=True
    )

    quantity = QuantitySerializer(many=True, required=False)

    class Meta:
        model = Order
        fields = "__all__"
    
    def to_internal_value(self, data):
        internal_representation = data.copy()
        if internal_representation.__contains__("quantity"):
            quantity = json.loads(internal_representation.pop('quantity')[0])
            internal_representation = super().to_internal_value(internal_representation)
            internal_representation['quantity'] = quantity
        else:
            internal_representation = super().to_internal_value(internal_representation)
        return internal_representation

    def create(self, validated_data):
        return create_update_order(validated_data)

    def update(self, instance, validated_data):
        if validated_data.get("quantity", False) and validated_data.get("menu_items", False):
            return create_update_order(validated_data, instance.pk)
        return super().update(instance, validated_data)
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["quantity"] = {str(item.id): OrderMenu.objects.get(order_id=instance.id, menu_id=item.id).quantity for item in instance.menu_items.all()}
        for field in ["ordered_at", "prepared_at", "delivered_at"]:
            representation[field] = format_date(getattr(instance, field))
        return representation

class DashboardSerializer(serializers.Serializer):
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    frequency = serializers.CharField(max_length=5)