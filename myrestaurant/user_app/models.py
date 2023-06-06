from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.contrib.auth.password_validation import validate_password
import logging

logger = logging.getLogger(__name__)


class MyUserManager(BaseUserManager):
    # Defines methods to create users and superusers for custom MyUser model.

    def create_user(self, username, password=None, **kwargs):
        
        # Require username field
        if not username:
            raise ValueError('Users must have a username')
            
        user = self.model(
            username=username.lower(),
            **kwargs
        )

        validate_password(password)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, password=None, **kwargs):

        user = self.create_user(
            username.lower(),
            password=password,
            **kwargs,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class MyUser(AbstractBaseUser, PermissionsMixin):
    # Custom user model
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=255, unique=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

    class Meta:
        db_table = "myuser"


class MyStaff(models.Model):
    roles = [
        ("SALES", "Sales"),             # orders, dashboard
        ("MANAGER", "Manager"),         # all
        ("CHEF", "Chef")                # inventory, menu
    ]
    id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    join_date = models.DateField(auto_now_add=True)
    role = models.CharField(choices=roles, max_length=50, blank=True)

    class Meta:
        db_table = "mystaff"

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
        