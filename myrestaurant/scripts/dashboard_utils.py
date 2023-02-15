from datetime import datetime
from django.db import connection
import logging

logger = logging.getLogger(__name__)

cursor = connection.cursor()

def get_profit(start_date, end_date):
    sql = """
        SELECT menu.price, menu.ingredients_cost
        FROM orders_menu_items
        LEFT JOIN orders
            ON orders_menu_items.order_id = orders.id
        LEFT JOIN menu
            ON orders_menu_items.menu_id = menu.id
        WHERE orders.ordered_at >= %s AND orders.ordered_at <= %s;
    """
    cursor.execute(sql, [start_date, end_date])
    results = cursor.fetchall()

    return sum([item[0]-item[1] for item in results])


def run():
    start = datetime.strptime("09-02-2023 23:59:59", "%d-%m-%Y %H:%M:%S")
    end = datetime.strptime("16-02-2023 23:59:59", "%d-%m-%Y %H:%M:%S")
    get_profit(start, end)