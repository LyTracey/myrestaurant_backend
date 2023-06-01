from django.test import TestCase, Client
from user_app.models import MyStaff, MyUser
from myrestaurant_app.models import Order
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
        
        # Create inventory item
        inventory_response = client.post("/myrestaurant/inventory/", {"ingredient": "Chicken", "quantity": 10, "unit_price": 4.50})
        ingredient = inventory_response.data

        # Create menu item
        menu_response = client.post("/myrestaurant/menu/", 
            {"title": "Roast chicken", "description": "Classic sunday roast.", "ingredients": [ingredient['id']], "units": json.dumps({ingredient['id']: 2}), "price": 8.20 })
        menu_item = menu_response.data

        # Create order item
        orders_response = client.post("/myrestaurant/orders/", 
            {"menu_items": [menu_item['id']], "quantity": json.dumps({menu_item['id']: 5}) })
        order = orders_response.data

    def setUp(self) -> None:
        """
            Get and set authentication credentials for every test.
        """

        login_response = client.post("/user/login/", {"username": "admin", "password": "AdminAuth9"})
        self.client.defaults["HTTP_AUTHORIZATION"] = f"Bearer {login_response.data['access']}"
        self.client.defaults["HTTP_CONTENT_TYPE"] = "multipart/form-data"
       
    def test_prepared_before_delivered(self):
        """
            Test that the order must be prepared before it is delivered.
        """

        order = Order.objects.first()
        response = self.client.patch(f"/myrestaurant/orders/{order.id}/", {"delivered": True})
        self.assertEqual(response.data["error"], "Please make sure order is prepared first.")


    
    def test_prepared_delivered_before_complete(self):
        """
            Test that the order must be prepared and delivered before it is complete.
        """

        order = Order.objects.first()
        response = self.client.patch(f"/myrestaurant/orders/{order.id}/", {"complete": True})
        self.assertEqual(response.data["error"], "Please make sure order is prepared and delivered first.")