from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from rest_framework.authtoken.models import Token
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from datetime import date

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class MyUserManager(BaseUserManager):
    # Defines methods to create users and superusers for custom MyUser model.
    def create_user(self, email, password=None, **kwargs):
        
        # Require email field
        if not email:
            raise ValueError('Users must have an email address')
            
        user = self.model(
            email=self.normalize_email(email),
            **kwargs
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **kwargs):

        user = self.create_user(
            email,
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
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        db_table = "myuser"


class MyStaff(models.Model):
    roles = [
        ("SALES", "Sales"),
        ("MANAGER", "Manager"),
        ("CHEF", "Chef"),
        ("OTHER", "Other")
    ]
    id = models.BigAutoField(primary_key=True)
    staff = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    join_date = models.DateField(auto_now_add=True)
    role = models.CharField(choices=roles, max_length=50, blank=True)

    class Meta:
        db_table = "mystaff"