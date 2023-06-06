from django.test import TestCase
from user_app.models import MyUser, MyStaff
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from user_app.serializers import MyStaffSerializer
import logging

logger = logging.getLogger(__name__)


class MyUserModelTestCase (TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        user = MyUser.objects.create_user(username="abc", password="Testing3", is_staff=True)

    def test_limit_roles(self) -> None:
        """
            Test that the value of MyStaff.role is limited to a predefined set of values (i.e. MANAGER, CHEF, SALES, ADMIN). Any other values should raise a ValidationError.
        """
        user = MyUser.objects.get(username="abc")
        
        with self.assertRaises(ValidationError):
            MyStaff.objects.update_or_create(user_id=user.id, defaults={"role": "Baker"})

        updated_user, _ = MyStaff.objects.update_or_create(user_id=user.id, defaults={"role": "SALES"})
        self.assertEqual(updated_user.role, "SALES")


    def test_myuser_password_validation(self) -> None:
        """
            Test that user passwords must follow a certain regex pattern i.e. at least 1 captial letter, 1 lowercase letter, 1 number, and be at least 6 characters.
        """
        
        with self.assertRaises(ValidationError):
            MyUser.objects.create_user(username="abc", password="CreaTe")

        with self.assertRaises(ValidationError):
            MyUser.objects.create_user(username="xyz", password="create")

        with self.assertRaises(ValidationError):
            MyUser.objects.create_user(username="qrs", password="create7")



    def test_mystaff_cascades(self) -> None:
        """
            Test that instance in mystaff deletes if the related instance in myuser is deleted.
        """
        user = MyUser.objects.create_user(username="croissant", password="Yum!76", is_staff=True)
        staff = MyStaff.objects.get(user_id=user.id)
        self.assertIsInstance(staff, MyStaff)

        user.delete()
    
        with self.assertRaises(ObjectDoesNotExist):
             MyStaff.objects.get(user=user.id)

        