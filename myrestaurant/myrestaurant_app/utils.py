import logging
import os
from django.conf import settings
from django.utils.text import slugify
import json
from . import models
from django.db.models.signals import post_save
from django.dispatch import receiver


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


# Update inventory when order is placed
@receiver(post_save, sender=models.Order)
def update_units_available(send, instance):
    # When order placed
    # Get units available
    # Get menu_items and quantity of each ingredient needed
    # Minus quantity of units needed from units available for each ingredient

    # Get inventory items for order

    items = instance.orders_menu
    

    pass