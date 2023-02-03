from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

class Customer(models.Model):
    customer_id = models.BigAutoField(primary_key=True)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    dob = models.DateField(default=None)

    class Meta:
        db_table = "customers"

    def __str__(self):
        return str(self.customer_id)
