import logging
import os
from django.conf import settings
from django.utils.text import slugify
import json
from decimal import Decimal


logger = logging.getLogger(__name__)

# Slugify
def auto_slug(self, property: str):
    if not self.slug:
        self.slug = slugify(property)

# Function to request overwriting file
def overwrite(serializer):
    if serializer.data["overwrite"]:
        file = str(serializer.data['image'])
        logger.info(f"User wants to overwrite file {file}.")
        original_image_url = os.path.join(settings.MEDIA_ROOT, "menu", file)
        os.remove(original_image_url)
        logger.info("Original file removed.")


# Function to convert list input into JSON string
def list_to_JSON(keys, values):
    if isinstance(values, list):
        json_string = json.dumps({item[0]: int(item[1]) for item in  zip(keys, values) })
        return json_string
    return values

# Function to process units field in  Menu Inventory many-to-many relationship
def create_update_menu(validated_data, model, through_model, pk=None):
    ingredients = validated_data.pop('ingredients')
    units = validated_data.pop('units')

    # Calculate ingredients_cost
    ingredients_cost = sum([item.unit_price * Decimal(units[str(item.pk)]) for item in ingredients])

    # Create menu model instance
    menu_item, created = model.objects.update_or_create(pk=pk, defaults={**validated_data, "ingredients_cost": ingredients_cost})

    # Delete entries in menuInventory
    menu_item.ingredients.clear()

    # Create menu_inventory data instances
    for item in ingredients:
        menu_item
        obj = through_model.objects.create(
            menu_id=menu_item,
            inventory_id=item,
            units=units[str(item.pk)]
        )
    
    return menu_item


def run():
    pass