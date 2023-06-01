import logging
from datetime import datetime
from .dashboard_utils import get_availability

logger = logging.getLogger(__name__)
        

def create_update_menu(validated_data, model, through_model, pk=None):
    """
        Function to process units field in  Menu Inventory many-to-many relationship
    """
    try:
        ingredients = validated_data.pop('ingredients')
    except:
        ingredients = []
    units = validated_data.pop('units')

    # Create menu model instance
    menu_item, created = model.objects.update_or_create(pk=pk, defaults={**validated_data})
    
    # Delete entries in menuInventory
    through_model.objects.filter(menu_id=pk).delete()

    # Create menu_inventory data instances
    for item in ingredients:
        obj = through_model.objects.create(
            menu_id=menu_item,
            inventory_id=item,
            units=units[str(item.pk)]
        )
    
    # Add available_quantity field
    menu_item.available_quantity = get_availability(menu_item)
    menu_item.save()
    
    return menu_item


def create_update_order(validated_data, model, through_model, inventory_model, menu_model, pk=None):
    menu_items = validated_data.pop('menu_items')
    quantity = validated_data.pop('quantity')

    # Create order model instance
    order, created = model.objects.update_or_create(pk=pk, defaults={**validated_data})

    # Add back inventory items before deleting
    if not created:
        previous_quantities = {k: v for k, v in order.ordermenu_set.values_list("menu_id", "quantity")}
        previous_menu_items = menu_model.objects.filter(pk__in=previous_quantities.keys())
        for item in previous_menu_items:
            inventory_items = item.menuinventory_set.values_list("inventory_id", "units")
            previous_units_used = {k: v*previous_quantities[item.id] for k, v in inventory_items}
            for id in previous_units_used.keys():
                obj = inventory_model.objects.get(id=id)
                obj.quantity = obj.quantity + previous_units_used[id]
                obj.save()

    # Delete entries in OrderMenu
    through_model.objects.filter(order_id=pk).delete()

    # Create order_menu instances and update inventory
    for item in menu_items:
        obj = through_model.objects.create(
            order_id=order,
            menu_id=item,
            quantity=quantity[str(item.pk)]
        )

        inventory_items = item.menuinventory_set.values_list("inventory_id", "units")
        units_used = {k: v*quantity[str(item.pk)] for k, v in inventory_items}
        for id in units_used.keys():
            obj = inventory_model.objects.get(id=id)
            try:
                obj.quantity = obj.quantity - units_used[id]
                obj.save()
            except:
                return "Order could not be processed as items are out of stock"
    
    # Update available quantity
    queryset = menu_model.objects.all()
    for item in queryset:
        item.save()

    return order

def format_date(date):
    if date:
        return datetime.strftime(date, "%Y-%m-%d %H:%M:%S")
    return None

def run():
    pass