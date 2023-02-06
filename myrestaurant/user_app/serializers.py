from rest_framework import serializers
from .models import MyUser

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['email', 'password']

