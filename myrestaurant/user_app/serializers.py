from rest_framework import serializers
from . import models

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Customer
        fields = ["customer_id", "email", "phone", "dob"]
