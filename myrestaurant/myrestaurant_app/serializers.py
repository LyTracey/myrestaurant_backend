from rest_framework import serializers
from . import models

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Menu
        fields = "__all__"
        lookup_field = "slug"

class OrderSerializer(serializers.ModelSerializer):
    menu_items = serializers.PrimaryKeyRelatedField(
        many=True, queryset=models.Menu.objects.all(),
        style={'base_template': 'checkbox_multiple.html'})

    class Meta:
        model = models.Order
        fields = ["notes", "ordered_at", "menu_items"]


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Inventory
        fields = ["ingredient", "quantity", "unit_price", "image"]

class DashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Dashboard
        fields = ["order_statistics", "menu_statistics", "inventory_statistics"]
