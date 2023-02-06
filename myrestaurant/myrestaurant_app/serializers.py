from rest_framework import serializers
from . import models

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Order
        fields = ["order_id", "customer_id", "order_items", "notes", "ordered_at", "prepared", "prepared_at", "delivered", "delivered_at", "complete"]

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Menu
        fields = "__all__"
        lookup_field = "slug"

class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Inventory
        fields = ["ingredient", "slug", "quantity", "unit_price", "image"]

class DashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Dashboard
        fields = ["order_statistics", "menu_statistics", "inventory_statistics"]
