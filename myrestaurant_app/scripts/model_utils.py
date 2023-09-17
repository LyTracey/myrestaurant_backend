from django.utils.text import slugify

# Slugify
def auto_slug(self, property: str):
    if not self.slug:
        self.slug = slugify(property)
