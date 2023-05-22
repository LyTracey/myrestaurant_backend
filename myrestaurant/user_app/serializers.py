from rest_framework import serializers
from rest_framework.fields import empty
from .models import MyUser, MyStaff
import logging
from django.contrib.auth.password_validation import validate_password
from rest_framework.serializers import ValidationError

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
        fields = ["role"]


class ProfileSerializer(serializers.ModelSerializer):

    mystaff = MyStaffSerializer(write_only=True)

    class Meta:
        model = MyUser
        fields = ["username", "is_staff", "mystaff"]
        depth = 2
        read_only_fields = ["username"]

    def to_internal_value(self, data):
        logger.debug(data)
        internal_value = data.copy()
        if data.__contains__("role"):
            role = internal_value.pop("role")[0]
            internal_value = super().to_internal_value(data)
            internal_value["role"] = role
        else:
            internal_value = super().to_internal_value(data)
        return internal_value

    def update(self, instance, validated_data):
        data = validated_data.copy()
        if validated_data.get("role"):
            role = data.pop("role")
            staff, staff_created = MyStaff.objects.update_or_create(user_id=instance.pk, defaults={"role": role})
        user, user_created = MyUser.objects.update_or_create(pk=instance.pk, defaults=data)
        return user

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.is_staff:
            staff = MyStaff.objects.get(user_id=instance.pk)
            representation["join_date"] = staff.join_date
            representation["role"] = staff.role
        return representation



