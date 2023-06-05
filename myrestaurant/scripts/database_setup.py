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
    MyUser.objects.all().delete()


def load_data(json_file, model_func, related_model=None, **kwargs):
    """
        Populates the database with hard-coded data as defined under fixtures
        directories in apps.
    """

    # Read json file
    data = json.load(json_file)
    MODEL_INSTANCE_FIELDS = ["ingredients", "menu_items"]

    # Create objs from json file
    for obj in data:
        pk = obj.get("id")

        if kwargs.get("model"):
            obj_dict = obj.copy()

            # Get list of instances from list of pks
            for key in obj_dict.keys():
                if key in MODEL_INSTANCE_FIELDS:
                    obj_dict[key] = related_model.objects.filter(id__in=obj[key])

            model_func(obj_dict, **kwargs, pk=pk)
        else:
            model_func(**obj, **kwargs)


def run():
    # Clear database
    flush_db()

    # Read json files
    inventory_json = open("scripts/data/inventory.json")
    menu_json = open("scripts/data/menu.json")
    orders_json = open("scripts/data/orders.json")

    # Load data into database
    load_data(inventory_json, Inventory.objects.create)
    load_data(menu_json, create_update_menu, Inventory, model=Menu, through_model=MenuInventory)
    load_data(orders_json, create_update_order, Menu, model=Order, through_model=OrderMenu, inventory_model=Inventory, menu_model=Menu)

    