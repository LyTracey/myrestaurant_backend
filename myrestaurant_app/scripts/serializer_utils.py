import logging
from datetime import datetime
from .dashboard_utils import get_availability
from myrestaurant_app.models import Order, Menu, Inventory, OrderMenu, MenuInventory
from typing import Type

logger = logging.getLogger(__name__)

def calculate_menu_availability ():
    """
        Calculate available quantities of menu items.
    """
    queryset = Menu.objects.all()
    for item in queryset:
        item.available_quantity = get_availability(item)
        item.save()


def return_ingredients (order: Type[Order]) -> None:
    """
        Add ingredients of order back to inventory.
    """

    order_menu_quantities = {k: v for k, v in order.ordermenu_set.values_list("menu_id", "quantity")}
    order_menu_items = Menu.objects.filter(pk__in=order_menu_quantities.keys())

    for item in order_menu_items:
        inventory_items = item.menuinventory_set.values_list("inventory_id", "units")
        inventory_units_used = {k: v*order_menu_quantities[item.id] for k, v in inventory_items}

        for id in inventory_units_used.keys():
            obj = Inventory.objects.get(id=id)
            obj.quantity = obj.quantity + inventory_units_used[id]
            obj.save()


def create_update_menu (validated_data, pk=None):
    """
        Function to process units field in  Menu Inventory many-to-many relationship.
    """
    try:
        ingredients = validated_data.pop('ingredients')
    except:
        ingredients = []
    units = validated_data.pop('units')

    # Create menu model instance
    menu_item, _ = Menu.objects.update_or_create(pk=pk, defaults={**validated_data})
    
    # Delete entries in menuInventory
    MenuInventory.objects.filter(menu_id=pk).delete()

    # Create menu_inventory data instances
    for item in ingredients:
        MenuInventory.objects.create(
            menu_id=menu_item,
            inventory_id=item,
            units=units[str(item.pk)]
        )
    
    # Add available_quantity field
    menu_item.available_quantity = get_availability(menu_item)
    menu_item.save()
    
    return menu_item


def create_update_order (validated_data, pk=None):
    menu_items = validated_data.pop('menu_items')
    quantity = validated_data.pop('quantity')

    # Create order model instance
    order, created = Order.objects.update_or_create(pk=pk, defaults={**validated_data})

    # Add back inventory items before deleting OrderMenu entries
    if not created:
        return_ingredients(order)

        # Delete entries in OrderMenu
        OrderMenu.objects.filter(order_id=pk).delete()

    # Create order_menu instances and update inventory
    for item in menu_items:
        obj = OrderMenu.objects.create(
            order_id=order,
            menu_id=item,
            quantity=quantity[str(item.pk)]
        )

        inventory_items = item.menuinventory_set.values_list("inventory_id", "units")
        units_used = {k: v*quantity[str(item.pk)] for k, v in inventory_items}

        for id in units_used.keys():
            obj = Inventory.objects.get(id=id)
            try:
                obj.quantity = obj.quantity - units_used[id]
                obj.save()
            except:
                return "Order could not be processed as items are out of stock."
    
    # Update available quantity
    calculate_menu_availability()

    return order





def format_date(date):
    if date:
        return datetime.strftime(date, "%Y-%m-%d %H:%M:%S")
    return None

def run():
    pass