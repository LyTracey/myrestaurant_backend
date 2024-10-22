from django.utils.text import slugify

# Slugify
def auto_slug(self, property: str):
    if not self.id:
        self.id = slugify(property)
