from rest_framework import serializers
from .models import MyUser, MyStaff
import logging

logger = logging.getLogger(__name__)

class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ["email", "password", "is_staff"]

    def create(self, validated_data):
        return MyUser.objects.create_user(**validated_data)

class MyStaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyStaff
        fields = "__all__"

