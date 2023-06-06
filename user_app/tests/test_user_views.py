from django.test import TestCase, Client
from user_app.models import MyUser
import logging
import time

LOGGER = logging.getLogger(__name__)

c = Client()

class MyUserViewTestCase(TestCase):
    
    @classmethod
    def setUpTestData(cls) -> None:
        c.post("/user/register/", {"username": "peach", "password": "Grape8", "is_staff": True})
        
    def test_password_hashed(self) -> None:
        """
            Test user password gets hashed when submitted through client.
        """
        user = MyUser.objects.get(username="peach")
        self.assertNotEqual(user.password, "Grape8")


    def test_login_staff(self) -> None:
        """
            Test login view returns whether the user is_staff.
        """
        
        response = self.client.post("/user/login/", {"username": "peach", "password": "Grape8"})
        self.assertEqual(response.data['isStaff'], True)

    
    def test_last_login_updates(self) -> None:
        """
            Test last_login field updates when user successfully logs in.
        """

        # First login and get last_login
        self.client.post("/user/login/", {"username": "peach", "password": "Grape8"})
        user = MyUser.objects.get(username="peach")
        previous_last_login = user.last_login
        
        # Wait for 1 second
        time.sleep(1)

        # Second login and get last_login
        self.client.post("/user/login/", {"username": "peach", "password": "Grape8"})
        user = MyUser.objects.get(username="peach")
        current_last_login = user.last_login

        # Compare datetimestamps
        self.assertNotEqual(previous_last_login, current_last_login)