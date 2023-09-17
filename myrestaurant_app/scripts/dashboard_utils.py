from myrestaurant_app.models import Inventory, Order, Menu
from datetime import datetime as dt
import datetime
import pandas as pd
from django.db.models import QuerySet
import logging
from itertools import chain

logger = logging.getLogger(__name__)


def get_max_dates():
    """
        Return max order date range - earliest order to current datetime.
    """
    
    try:
        start = Order.objects.earliest("ordered_at").ordered_at
    except:
        start = dt.now()

    return [start, dt.now()]


START_DATE, END_DATE = get_max_dates()

def str_to_datetime(start_date, end_date):
    if isinstance(start_date, str):
        start_date = dt.strptime(start_date, "%Y-%m-%d")
    
    if isinstance(end_date, str):
        end_date = dt.strptime(end_date, "%Y-%m-%d") + datetime.timedelta(days=1)
    
    return start_date, end_date


def get_revenue(start_date=START_DATE, end_date=END_DATE, frequency="B") -> list[dict]:
    """
        Return revenue within date range if specified, grouped by frequency (default 1 week).
    """

    start_date, end_date = str_to_datetime(start_date, end_date)

    # Get orders
    orders: QuerySet = Order.objects.filter(ordered_at__range=[start_date, end_date])
    
    # Calculate revenue
    revenue: list[float] = [order.total_cost for order in orders]

    # Create dataframe
    df: pd.DataFrame = pd.DataFrame(columns=["date", "revenue"])
    df["date"]: pd.Series = pd.to_datetime(orders.values_list("ordered_at", flat=True), format="%Y-%m-%d %H:%M:%S")
    df["revenue"]: pd.Series = revenue

    # Sum revenues by frequecy period
    grouped_df = df.groupby(pd.Grouper(key="date", freq=frequency)).sum().reset_index()
    grouped_df["date"] = grouped_df["date"].dt.strftime('%d-%m-%Y')

    return grouped_df.round(2).to_dict(orient="records")


def get_profit(start_date=START_DATE, end_date=END_DATE, frequency="B"):
    """
        Return profit within date range if specified, grouped by frequency (default 1 week).
    """

    start_date, end_date = str_to_datetime(start_date, end_date)

    # Get orders in time range
    orders = Order.objects.filter(ordered_at__range=[start_date, end_date])

    # Calculate profit per order
    profit_per_order = [order.total_cost - sum(menu_item.quantity * menu_item.menu_id.ingredients_cost for menu_item in order.ordermenu_set.all()) for order in orders]

    # Create dataframe
    df: pd.DataFrame = pd.DataFrame(columns=["date", "profit"])
    df["date"]: pd.Series = pd.to_datetime(orders.values_list("ordered_at", flat=True), format="%Y-%m-%d %H:%M:%S")
    df["profit"]: pd.Series = profit_per_order

    # Sum profits by frequency period
    grouped_df = df.groupby(pd.Grouper(key="date", freq=frequency)).sum().reset_index()
    grouped_df["date"] = grouped_df["date"].dt.strftime('%d-%m-%Y')

    return grouped_df.round(2).to_dict(orient="records")


def get_item_sales(start_date=START_DATE, end_date=END_DATE):
    """
        Get each menu item and return the quantity sold in the specified timeframe.
    """

    start_date, end_date = str_to_datetime(start_date, end_date)

    orders = Order.objects.filter(ordered_at__range=([start_date, end_date]))
    menu = set(chain.from_iterable([(menu_item.menu_id for menu_item in order.ordermenu_set.all()) for order in orders]))

    return {menu_item.title: sum(order_item.quantity for order_item in menu_item.ordermenu_set.all()) for menu_item in menu}


def get_low_stock():
    """
        Get ingredients that are low in stock, defined as being below the threshold. The default threshold is 10. 
    """

    ingredient_quantities = [(inventory_item.ingredient, inventory_item.quantity, inventory_item.threshold) for inventory_item in Inventory.objects.all()]

    low_stock = [ingredient for ingredient, quantity, threshold in ingredient_quantities if quantity < threshold]

    return low_stock


def get_out_of_stock():
    """
        Get menu_items that are out of stock. If there are insufficient ingredients available 
        in the inventory to make the menu item, the menu_item is out of stock.
    """

    return [menu_item.title for menu_item in Menu.objects.all() if menu_item.available_quantity == 0]


def get_availability(instance):
    """
        Get the available quantity of menu_items (in theory) with the available ingredients in stock.
    """
    
    return min([inventory_item.inventory_id.quantity // inventory_item.units for inventory_item in instance.menuinventory_set.all()], default=0)


def summary_statistics(start_date=None, end_date=None, frequency=None):
    start_date, end_date = str_to_datetime(start_date, end_date)

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


# def run():
#     print(get_revenue())