from myrestaurant_app.models import Order, Menu, Inventory, MenuInventory, OrderMenu
from user_app.models import MyUser
import json
from myrestaurant_app.scripts.serializer_utils import create_update_menu, create_update_order
import logging

logger = logging.getLogger(__name__)

def flush_db():
    """
        Call to truncate all user-defined model tables. This is not reversible.
    """

    Order.objects.all().delete()
    Menu.objects.all().delete()
    Inventory.objects.all().delete()


def load_inventory_data(inventory_json):
    
    data = json.load(inventory_json)
    for inventory_obj_data in data:
        Inventory.objects.create(**inventory_obj_data)


def load_menu_data(menu_json):
    
    data = json.load(menu_json)
    for menu_obj_data in data:
        pk = menu_obj_data.get("id")

        new_menu_obj = menu_obj_data.copy()

        # Get list of instances of related models using listed pks
        new_menu_obj["ingredients"] = Inventory.objects.filter(id__in=menu_obj_data["ingredients"])

        create_update_menu(new_menu_obj, pk=pk)
        
        
def load_order_data(order_json):
    
    data = json.load(order_json)
    for order_obj_data in data:

        new_order_obj = order_obj_data.copy()

        # Get list of instances of related models using listed pks
        new_order_obj["menu_items"] = Menu.objects.filter(id__in=order_obj_data["menu_items"])

        create_update_order(new_order_obj)     


def run():
    # Clear database
    try:
        flush_db()
    except:
        logger.info("Could not flush database")

    # Read json files
    inventory_json = open("scripts/data/inventory.json")
    menu_json = open("scripts/data/menu.json")
    orders_json = open("scripts/data/orders.json")

    # Load data into database
    load_inventory_data(inventory_json)
    load_menu_data(menu_json)
    load_order_data(orders_json)

    