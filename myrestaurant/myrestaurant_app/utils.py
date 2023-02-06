import logging
import os
from django.conf import settings
from django.utils.text import slugify

logger = logging.getLogger("general")

# Slugify
def auto_slug(self, property):
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
