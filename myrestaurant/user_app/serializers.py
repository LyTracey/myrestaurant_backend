from rest_framework import serializers
from .models import MyUser, MyStaff
import logging

logger = logging.getLogger(__name__)

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ["username", "password", "is_staff"]

    def create(self, validated_data):
        return MyUser.objects.create_user(**validated_data)
    

class MyStaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyStaff
        fields = "__all__"

class ProfileSerializer(serializers.ModelSerializer):
    mystaff = MyStaffSerializer(read_only=True)

    class Meta:
        model = MyUser
        fields = ["username", "is_staff", "mystaff"]
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.is_staff:
            representation["join_date"] = instance.mystaff.join_date
            representation["role"] = instance.mystaff.role
        del representation["mystaff"]
        return representation



