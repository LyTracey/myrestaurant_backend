from .dashboard_utils import get_availability

# Check if quantity ordered is less than available quantity
def ordered_lte_available(quantity, menu_model):
    for item in quantity.keys():
        menu_obj = menu_model.objects.get(pk=int(item))
        if get_availability(menu_obj) < quantity[item]:
            return False
    return True