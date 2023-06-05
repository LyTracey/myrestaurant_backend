from django.contrib import admin
from .models import Inventory, Menu, Order, OrderMenu, MenuInventory

admin.site.register(Inventory)
admin.site.register(Menu)
admin.site.register(Order)
admin.site.register(OrderMenu)
admin.site.register(MenuInventory)