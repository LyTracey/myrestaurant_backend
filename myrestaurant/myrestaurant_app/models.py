from django.db import models
from .scripts.model_utils import auto_slug
from django.core.validators import MinValueValidator
import logging

logger = logging.getLogger(__name__)

class Inventory(models.Model):
    id = models.BigAutoField(primary_key=True)
    ingredient = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(unique=True, max_length=30, blank=True)
    quantity = models.PositiveSmallIntegerField(default=0)
    unit_price = models.DecimalField(max_digits=5, decimal_places=2, default=None, blank=True)
    image = models.ImageField(upload_to='inventory', blank=True)
    
    class Meta:
        db_table = "inventory"
    
    def save(self, *args, **kwargs):
        auto_slug(self, self.ingredient)
        super().save(*args, **kwargs)
         
    def __str__(self):
        return self.ingredient


class Menu(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True, max_length=30, blank=True)
    image = models.ImageField(upload_to='menu', blank=True, null=True)
    description = models.TextField(blank=True)
    ingredients = models.ManyToManyField(Inventory, through="MenuInventory")
    ingredients_cost = models.DecimalField(max_digits=5, default=None, null=True, blank=True, decimal_places=2)
    price = models.DecimalField(max_digits=5 , decimal_places=2, default=None, blank=True, null=True)
    available_quantity = models.PositiveSmallIntegerField(blank=True, default=0, validators=[MinValueValidator(0, message="unit is not a positive")])

    class Meta:
        db_table = "menu"

    def save(self, *args, **kwargs):
        auto_slug(self, self.title) 
        super().save(*args, **kwargs) 
            
    def __str__(self):
        return self.title


class Order(models.Model):
    id = models.BigAutoField(primary_key=True)
    menu_items = models.ManyToManyField(Menu, through="OrderMenu")
    notes = models.CharField(max_length=300, blank=True, null=True)
    ordered_at = models.DateTimeField(auto_now_add=True)
    prepared = models.BooleanField(default=False)
    prepared_at = models.DateTimeField(default=None, null=True)
    delivered = models.BooleanField(default=False)
    delivered_at = models.DateTimeField(default=None, null=True)
    complete = models.BooleanField(default=False, null=True)
    total_cost = models.DecimalField(max_digits=5, default=None, blank=True, null=True, decimal_places=2)

    class Meta:
        db_table = "orders"
        ordering = ["-ordered_at"]


# Custom through models
class MenuInventory(models.Model):
    id = models.BigAutoField(primary_key=True)
    menu_id = models.ForeignKey(Menu, on_delete=models.CASCADE, db_column="menu_id")
    inventory_id = models.ForeignKey(Inventory, on_delete=models.CASCADE, db_column="inventory_id")
    units = models.DecimalField(max_digits=5, decimal_places=2, default=None, null=True, validators=[MinValueValidator(0, message="unit is not a positive")])

    class Meta:
        db_table = "menu_inventory"
    

class OrderMenu(models.Model):
    id = models.BigAutoField(primary_key=True)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE, db_column="order_id")
    menu_id = models.ForeignKey(Menu, on_delete=models.CASCADE, db_column="menu_id")
    quantity = models.PositiveSmallIntegerField(default=1, validators=[MinValueValidator(0, message="unit is not a positive")])

    class Meta:
        db_table = "orders_menu"