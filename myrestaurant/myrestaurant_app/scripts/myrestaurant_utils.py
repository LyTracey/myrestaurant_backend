import logging
import os
from django.conf import settings
from django.utils.text import slugify
import json


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
    

def run():
    pass