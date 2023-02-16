from datetime import datetime
from django.db import connection
import logging


logger = logging.getLogger(__name__)

cursor = connection.cursor()

def get_profit(start_date, end_date):
    sql = """
        SELECT menu.price, orders_menu.quantity, menu.ingredients_cost
        FROM orders_menu
        LEFT JOIN orders
            ON orders_menu.order_id = orders.id
        LEFT JOIN menu
            ON orders_menu.menu_id = menu.id
        WHERE orders.ordered_at >= %s AND orders.ordered_at <= %s;
    """
    cursor.execute(sql, [start_date, end_date])
    results = cursor.fetchall()

    return sum([(item[0]-item[2])*item[1] for item in results])


def running_low(threshold):
    # Get quantity available for each item in inventory
    # Calculate average quantity needed per day for each item
    # If amount available < quantity needed per day + x%, return in running_low list
    sql = """
        SELECT ingredient
        FROM inventory
        WHERE quantity < %s;
    """
    cursor.execute(sql, [threshold])
    results = [item[0] for item in cursor.fetchall()]
    return results


def out_of_stock(menu_id):
    # Get menu items
    # Get units needed for each ingredient
    # Get units available for each ingredient
    # If units needed > units available, return in out_of_stock list
    pass

# def total(property, model):
#     # Get sum of property
#     sql = f"""
#         SELECT SUM({ property })
#         FROM { model };
#     """
#     cursor.execute(sql)
#     results = cursor.fetchone()[0]
#     return results


# def percentage_change():
#     return None






def item_sales(key, model, item):
    # Get orders in timeframe
    # Get menu items in each order
    # Count the quantity sold for each menu item
    pass

def summary_statistics():
    pass


def run():
    start = datetime.strptime("09-02-2023 23:59:59", "%d-%m-%Y %H:%M:%S")
    end = datetime.strptime("16-02-2023 23:59:59", "%d-%m-%Y %H:%M:%S")
    running_low(11)