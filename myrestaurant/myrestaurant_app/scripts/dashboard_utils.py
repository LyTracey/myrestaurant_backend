from datetime import datetime
from django.db import connection
import logging
from myrestaurant_app.models import Inventory


logger = logging.getLogger(__name__)

cursor = connection.cursor()

def get_max_dates():

    sql = """
        SELECT MIN(ordered_at)
        FROM orders;
    """

    cursor.execute(sql)
    start = cursor.fetchone()[0]

    return [start, datetime.now()]


def get_revenue(start_date=None, end_date=None):
    sql = """
        SELECT SUM(menu.price * orders_menu.quantity)
        FROM orders_menu
        LEFT JOIN orders
            ON orders_menu.order_id = orders.id
        LEFT JOIN menu
            ON orders_menu.menu_id = menu.id
        WHERE orders.ordered_at BETWEEN %s AND %s;
    """

    if not all([start_date, end_date]):
        start_date, end_date = get_max_dates()


    cursor.execute(sql, [start_date, end_date])

    result = cursor.fetchone()[0]
    if result:
        return result
    
    return 0


def get_profit(start_date=None, end_date=None):
    sql = """
        SELECT menu.price, orders_menu.quantity, menu.ingredients_cost
        FROM orders_menu
        LEFT JOIN orders
            ON orders_menu.order_id = orders.id
        LEFT JOIN menu
            ON orders_menu.menu_id = menu.id
        WHERE orders.ordered_at BETWEEN %s AND %s;
    """
    if not all([start_date, end_date]):
        start_date, end_date = get_max_dates()

    cursor.execute(sql, [start_date, end_date])

    return sum((price - cost) * quantity for price, quantity, cost in cursor.fetchall())


def get_item_sales(start_date=None, end_date=None):
    # Get orders in timeframe
    # Get menu items in each order
    # Count the quantity sold for each menu item
    sql = """
        SELECT menu.title, SUM(orders_menu.quantity)
        FROM orders_menu
        JOIN orders
            ON orders_menu.order_id = orders.id
        JOIN menu
            ON orders_menu.menu_id = menu.id
        WHERE orders.ordered_at BETWEEN %s and %s
        GROUP BY orders_menu.menu_id;
    """
    if not all([start_date, end_date]):
        start_date, end_date = get_max_dates()
        
    cursor.execute(sql, [start_date, end_date])

    return {id: sold for id, sold in cursor.fetchall()}


def get_low_stock(default=10, threshold={}):
    # Get quantity available for each item in inventory
    # Set global default quantity threshold
    # Set individual threshold in dict (optional)

    sql = """
        SELECT ingredient, quantity
        FROM inventory;
    """

    cursor.execute(sql)

    low_stock = []

    for ingredient, quantity in cursor.fetchall():
        try: 
            if quantity < threshold[ingredient]:
                low_stock.append(ingredient)
        except:
            if quantity < default:
                low_stock.append(ingredient)
    
    return low_stock


def get_out_of_stock():
    # For each menu item, if units needed > units available for any ingredient, add to out_of_stock
    
    sql = """
        SELECT menu.title, inventory.quantity, menu_inventory.units
        FROM menu_inventory
        LEFT JOIN menu
            ON menu_inventory.menu_id = menu.id
        LEFT JOIN inventory
            ON menu_inventory.inventory_id = inventory.id;
    """

    cursor.execute(sql)
    
    out_of_stock = set([title for title, units, quantity in cursor.fetchall() if units < quantity])
    
    return out_of_stock


def summary_statistics(start_date=None, end_date=None):
        low_stock = get_low_stock()
        out_of_stock = get_out_of_stock()
        revenue = get_revenue(start_date, end_date)
        profit = get_profit(start_date, end_date)
        sales = get_item_sales(start_date, end_date)
        return {
            "revenue": revenue,
            "profit": profit,
            "low_stock": low_stock,
            "out_of_stock": out_of_stock,
            "sales": sales
        }



# def run():
#     start = datetime.strptime("09-02-2023 23:59:59", "%d-%m-%Y %H:%M:%S")
#     end = datetime.strptime("16-02-2023 23:59:59", "%d-%m-%Y %H:%M:%S")
#     get_revenue(start, end)