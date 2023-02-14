from django.db import models
from .utils import auto_slug


class Inventory(models.Model):
    id = models.BigAutoField(primary_key=True)
    ingredient = models.CharField(max_length=30)
    slug = models.SlugField(unique=True, max_length=30, blank=True)
    quantity = models.IntegerField(default=0)
    unit_price = models.DecimalField(max_digits=5, decimal_places=2, default=None, blank=True)
    image = models.ImageField(upload_to='inventory', blank=True)
    
    def save(self, *args, **kwargs):
        auto_slug(self, self.ingredient)
        super().save(*args, **kwargs)
        
    class Meta:
        verbose_name_plural = "Inventory"
        db_table = "inventory"
    
    def __str__(self):
        return self.ingredient


class Menu(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, max_length=30, blank=True)
    image = models.ImageField(upload_to='menu', blank=True, null=True)
    description = models.TextField(blank=True)
    ingredients = models.ManyToManyField(Inventory, through="MenuInventory", related_name="ingredients")
    price = models.DecimalField(max_digits=5 , decimal_places=2, default=None, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Menu"
        db_table = "menu"

    def save(self, *args, **kwargs):
        auto_slug(self, self.title)
        super().save(*args, **kwargs)
            
    def __str__(self):
        return self.title


class MenuInventory(models.Model):
    menu_id = models.ForeignKey(Menu, on_delete=models.CASCADE, db_column="menu_id", related_name="menu")
    inventory_id = models.ForeignKey(Inventory, on_delete=models.CASCADE, db_column="inventory_id", related_name="inventory")
    units = models.PositiveSmallIntegerField(default=None, null=True)

    class Meta:
        db_table = "menu_inventory"
    

class Order(models.Model):
    id = models.BigAutoField(primary_key=True)
    menu_items = models.ManyToManyField(Menu, related_name="orders")
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


class Dashboard(models.Model):
    id = models.BigAutoField(primary_key=True)
    order_statistics = models.JSONField(default=dict, null=True)
    inventory_statistics = models.JSONField(default=dict, null=True)
    menu_statistics = models.JSONField(default=dict, null=True)

    class Meta:
        db_table = "dashboard"