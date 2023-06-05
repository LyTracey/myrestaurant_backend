from datetime import datetime
from django.db import connection
import logging
import pandas as pd
# from myrestaurant_app.models import Menu

logger = logging.getLogger(__name__)

cursor = connection.cursor()

def get_max_dates() -> list[datetime]:

    sql = """
        SELECT MIN(ordered_at)
        FROM orders;
    """

    cursor.execute(sql)
    start = cursor.fetchone()[0]

    return [start, datetime.now()]


def get_revenue(start_date=None, end_date=None, frequency="1W"):
    sql = """
        SELECT orders.ordered_at AS date, menu.price * orders_menu.quantity AS revenue
        FROM orders_menu
        LEFT JOIN orders
            ON orders_menu.order_id = orders.id
        LEFT JOIN menu
            ON orders_menu.menu_id = menu.id
        WHERE orders.ordered_at BETWEEN %s AND %s;
    """

    if not all([start_date, end_date]):
        start_date, end_date = get_max_dates()
    


    df = pd.read_sql(sql, con=connection, params=[start_date, end_date], parse_dates=["date"])


    grouped_df = df.groupby(pd.Grouper(key="date", freq=frequency)).sum(numeric_only=True).reset_index()
    grouped_df["date"] = grouped_df["date"].astype("str")

    return grouped_df.round(2).to_dict(orient="records")


def get_profit(start_date=None, end_date=None, frequency="1W"):
    sql = """
        SELECT orders.ordered_at AS date, ((menu.price - menu.ingredients_cost) * orders_menu.quantity) AS profit
        FROM orders_menu
        LEFT JOIN orders
            ON orders_menu.order_id = orders.id
        LEFT JOIN menu
            ON orders_menu.menu_id = menu.id
        WHERE orders.ordered_at BETWEEN %s AND %s;
    """
    if not all([start_date, end_date]):
        start_date, end_date = get_max_dates()

    df = pd.read_sql(sql, con=connection, params=[start_date, end_date], parse_dates=["date"])

    grouped_df = df.groupby(pd.Grouper(key="date", freq=frequency)).sum(numeric_only=True).reset_index()
    grouped_df["date"] = grouped_df["date"].astype(str)
    

    return grouped_df.round(2).to_dict(orient="records")


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

def get_availability(instance):
    # Get the available quantity of menu_items (in theory) with the available ingredients in stock
    sql  = """
        SELECT inventory.quantity, menu_inventory.units
        FROM menu_inventory
        LEFT JOIN inventory
            ON menu_inventory.inventory_id = inventory.id
        WHERE menu_inventory.menu_id = %s;
    """

    cursor.execute(sql, [instance.id])

    available_quantity = min([(quantity // units) for quantity, units in cursor.fetchall()], default=0)

    return available_quantity
    


def summary_statistics(start_date=None, end_date=None, frequency=None):
        low_stock = get_low_stock()
        out_of_stock = get_out_of_stock()
        revenue = get_revenue(start_date, end_date, frequency)
        profit = get_profit(start_date, end_date, frequency)
        sales = get_item_sales(start_date, end_date)
        return {
            "revenue": revenue,
            "profit": profit,
            "low_stock": low_stock,
            "out_of_stock": out_of_stock,
            "sales": sales
        }



def run():
    # start_date = "2023-05-12 00:00:00"
    # end_date = "2023-05-14 00:00:00"
    print(get_revenue())
    # instance = Menu.objects.get(pk=20)
    # result = get_availability(instance)
    # print(result)