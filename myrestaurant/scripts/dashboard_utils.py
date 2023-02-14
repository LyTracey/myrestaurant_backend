from datetime import datetime
from django.db import connection
import logging

logger = logging.getLogger(__name__)

cursor = connection.cursor()

def get_profit(start_date, end_date):
    # Get orders in timeframe - need to convert to datetime?
    # Get menu items orders in each order and price of each menu_item
    # Get ingredients for each menu item ordered, units needed, and unit_price
    # Work out the difference

    sql = """
        SELECT orders_menu_items.menu_id, menu.price
        FROM orders
        JOIN orders_menu_items
            ON orders.id = orders_menu_items.order_id
        LEFT JOIN menu
            ON orders_menu_items.menu_id = menu.id
        WHERE orders.ordered_at >= %s AND orders.ordered_at <= %s;
    """
    cursor.execute(sql, [start_date, end_date])
    total_revenue = sum([item[1] for item in cursor.fetchall() if item[1] is not None])

    logger.info()



def run():
    start = datetime.strptime("09-02-2023 23:59:59", "%d-%m-%Y %H:%M:%S")
    end = datetime.strptime("12-02-2023 23:59:59", "%d-%m-%Y %H:%M:%S")
    get_profit(start, end)