from django.test import TestCase, Client
from myrestaurant_app.models import Order, Menu, Inventory
from user_app.models import MyStaff, MyUser
import logging
from rest_framework.test import APIClient, APITestCase, APIRequestFactory
import json
import urllib

logger = logging.getLogger(__name__)

client = APIClient()

class OrderViewTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls) -> None:

        # Create user to provide authentication and required permissions.
        user = MyUser.objects.create_user(username="admin", password="AdminAuth9", is_staff=True)
        user.mystaff.role = "MANAGER"
        user.mystaff.save()

        # Get access token and set headers
        login_response = client.post("/user/login/", {"username": "admin", "password": "AdminAuth9"})
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {login_response.data['access']}", HTTP_CONTENT_TYPE="multipart/form-data")
        
        inventory_response = client.post("/myrestaurant/inventory/", {"ingredient": "Chicken", "quantity": 10, "unit_price": 4.50})
        ingredient = inventory_response.data
        menu_response = client.post("/myrestaurant/menu/", 
            {"title": "Roast chicken", "description": "Classic sunday roast.", "ingredients": [ingredient['id']], "units": json.dumps({ingredient['id']: 2}) })
        
        menu_item = menu_response.data
        logger.debug(menu_item)
        # orders_response = client.post("/myrestaurant/orders/", {"menu_id": [menu_item['id']], "quantity": {menu_item['id']: 5}})
        # order = orders_response.data
    
    # def test_prepared_before_delivered(self):
    #     """
    #         Test that the order must be prepared before it is delivered.
    #     """
    #     order = Order.objects.first()
    #     logger.debug(order.__dict__)
    #     self.client.patch(f"/orders/{order.id}/", {"delivered": True})


    
    def test_prepared_delivered_before_complete(self):
        pass