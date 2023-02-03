from django.db import models
from .utils import auto_slug

class Inventory(models.Model):
    ingredient = models.CharField(max_length=30, primary_key=True, blank=False)
    slug = models.SlugField(unique=True, max_length=30, blank=True, null=True)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=5, decimal_places=2)
    image = models.ImageField(upload_to='inventory', blank=True)
    
    def save(self, *args, **kwargs):
        auto_slug(self)
        super().save(*args, **kwargs)
        
    class Meta:
        verbose_name_plural = "Inventory"
        db_table = "inventory"
    
    def __str__(self):
        return self.ingredient

class Menu(models.Model):
    title = models.CharField(primary_key=True, max_length=50)
    slug = models.SlugField(unique=True, max_length=30, blank=True)
    image = models.ImageField(upload_to='menu', blank=True, null=True)
    description = models.TextField()

    class Meta:
        verbose_name_plural = "Menu"
        db_table = "menu"

    def save(self, *args, **kwargs):
        auto_slug(self)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
class Order(models.Model):
    order_id = models.BigAutoField(primary_key=True)
    order_items = models.CharField(max_length=300)
    notes = models.CharField(max_length=300, blank=True, null=True)
    ordered_at = models.DateTimeField(auto_now_add=True)
    prepared = models.BooleanField(default=False)
    prepared_at = models.DateTimeField(default=None, null=True)
    delivered = models.BooleanField(default=False)
    delivered_at = models.DateTimeField(default=None, null=True)
    complete = models.BooleanField(default=False, null=True)

    class Meta:
        verbose_name_plural = "Orders"
        db_table = "orders"

    def __str__(self):
        return str(self.order_id)
