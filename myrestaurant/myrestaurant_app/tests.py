from django.test import TestCase
import logging
from myrestaurant_app.models import Inventory
from django.db import DataError

logger = logging.getLogger(__name__)

# class InventoryTests(TestCase):

class InventoryTestCase(TestCase):

    # fixtures = ["inventory.json"]

    def setUp(self):
        pass
    
    def test_quantity_gt0(self):
        with self.assertRaises(DataError):
            Inventory.objects.create(
                ingredient="Garlic",
                quantity=-14,
                unit_price=0.20,
            )
