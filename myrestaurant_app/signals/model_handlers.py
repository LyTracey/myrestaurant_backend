from django.db.models.signals import post_save
from django.dispatch import receiver
from myrestaurant_app.models import MenuInventory, OrderMenu
import logging

logger = logging.getLogger(__name__)

"""
    Signal to fire when instance is created/updated.
    Receiver to call relevant methods when instance is created/updated.
"""


@receiver(post_save, sender=MenuInventory, dispatch_uid="update_menuinventory")
def menu_handler(sender, instance, **kwargs):
    """
        Post-save handler for Menu model to calculate derived ingredients_cost field.
    """

    menu_item_ingredients = MenuInventory.objects.filter(menu_id=instance.menu_id)
    ingredients_cost = sum([ingredient.units * ingredient.inventory_id.unit_price for ingredient in menu_item_ingredients])
    
    instance.menu_id.ingredients_cost = ingredients_cost
    instance.menu_id.save()


@receiver(post_save, sender=OrderMenu)
def menu_handler(sender, instance, **kwargs):
    """
        Post-save handler for Order model to calculate derived total_cost field.
    """

    order_menu_items = sender.objects.filter(order_id=instance.order_id)
    total_cost = sum([menu_item.quantity * menu_item.menu_id.price for menu_item in order_menu_items])
   
    instance.order_id.total_cost = total_cost
    instance.order_id.save()



