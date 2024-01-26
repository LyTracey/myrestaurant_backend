from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from myrestaurant_app.models import MenuInventory, OrderMenu, Order, Inventory
import logging
from datetime import datetime
from myrestaurant_app.scripts.serializer_utils import calculate_menu_availability

logger = logging.getLogger(__name__)

"""
    Signal to fire when instance is created/updated.
    Receiver to call relevant methods when instance is created/updated.
"""


@receiver(post_save, sender=MenuInventory, dispatch_uid="update_menuinventory")
def menuinventory_handler(sender, instance, **kwargs):
    """
        Post-save handler for MenuInventory model to calculate derived ingredients_cost field.
    """

    menu_item_ingredients = MenuInventory.objects.filter(menu_id=instance.menu_id)
    ingredients_cost = sum([ingredient.units * ingredient.inventory_id.unit_price for ingredient in menu_item_ingredients])
    
    instance.menu_id.ingredients_cost = ingredients_cost
    instance.menu_id.save()


@receiver(post_save, sender=OrderMenu)
def ordermenu_handler(sender, instance, **kwargs):
    """
        Post-save handler for OrderMenu model to calculate derived total_cost field.
    """

    order_menu_items = sender.objects.filter(order_id=instance.order_id)
    total_cost = sum([menu_item.quantity * menu_item.menu_id.price for menu_item in order_menu_items])
   
    instance.order_id.total_cost = total_cost
    instance.order_id.save()


@receiver(pre_save, sender=Order)
def order_handler(sender, instance, **kwargs):
    """
        Pre-save handler for Order model to update prepared_at and ordered_at fields if their corresponding field is True.
        E.g. is prepared == True then prepared_at should be updated with the current time.
    """

    if instance.prepared == False:
        instance.prepared_at = None
    elif instance.prepared == True and instance.prepared_at is None:
        instance.prepared_at = datetime.now()

    if instance.delivered == False:
        instance.delivered_at = None
    elif instance.delivered == True and instance.delivered_at is None:
        instance.delivered_at = datetime.now()


    # if instance.delivered_at is not None:
    #     return
    # elif instance.delivered == True and instance.delivered_at is None:
    #     instance.delivered_at = datetime.now()
    # else:
    #     instance.delivered_at = None

@receiver(post_save, sender=Inventory)
def inventory_handler(sender, instance, **kwargs):
    calculate_menu_availability()
