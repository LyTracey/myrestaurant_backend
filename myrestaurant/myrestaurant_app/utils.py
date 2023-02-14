import logging
import os
from django.conf import settings
from django.utils.text import slugify
from django.db import connection
from datetime import datetime

logger = logging.getLogger(__name__)

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

## Dashboard utils

cursor = connection.cursor()

def total(model, property):
    # Get sum of property
    return None


def percentage_change():
    return None


def update_units_available():
    # When order placed
    # Get units available
    # Get menu_items and quantity of each ingredient needed
    # Minus quantity of units needed from units available for each ingredient
    pass


def out_of_stock(menu_id):
    # Get menu items
    # Get units needed for each ingredient
    # Get units available for each ingredient
    # If units needed > units available, return in out_of_stock list
    pass


def running_low():
    # Get quantity available for each item in inventory
    # Calculate average quantity needed per day for each item
    # If amount available < quantity needed per day + x%, return in running_low list
    pass


def item_sales(key, model, item):
    # Get orders in timeframe
    # Get menu items in each order
    # Count the quantity sold for each menu item
    pass

def get_profit(start_date, end_date):
    # Get orders in timeframe - need to convert to datetime?
    # Get menu items orders in each order and price of each menu_item
    # Get ingredients for each menu item ordered, units needed, and unit_price
    # Work out the difference

    sql = "SELECT * FROM orders WHERE delivered_at >= %s AND delivered_at <= %s"
    cursor.execute(sql, [start_date, end_date])
    orders = cursor.fetchall()
    ordered_items = {}
    logger.info(orders)

def summary_statistics():
    pass


if __name__ == "__main__":
    start = datetime.strptime("10-02-2023 23:59:59", "%d-%m-%y %H:%M:%S")
    end = datetime.strptime("10-02-2023 23:59:59", "%d-%m-%y %H:%M:%S")
    get_profit(start, end)
    