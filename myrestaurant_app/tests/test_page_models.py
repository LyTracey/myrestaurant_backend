from django.test import TestCase
import logging
from myrestaurant_app.models import Inventory
from django.db.utils import DataError

logger = logging.getLogger(__name__)


class InventoryModelTestCase(TestCase):

    @classmethod
    def setTestData(cls) -> None:
        ingredient = Inventory.objects.update_or_create(ingredient="Garlic", quantity=14, unit_price=0.20)
    
    def test_quantity_gt0(self) -> None:
        """
            Test that the quantity cannot be smaller than 0.
        """

        with self.assertRaises(DataError):
            Inventory.objects.update_or_create(ingredient="Garlic", quantity=-14, unit_price=0.20)
        
        ingredient  = Inventory.objects.get(ingredient="Garlic")
        self.assertIsInstance(ingredient, Inventory)


    
