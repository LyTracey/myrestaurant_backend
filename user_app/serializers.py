from rest_framework import serializers
from .models import MyUser, MyStaff
import logging
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['name'] = user.name
        # ...

        return token


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

class MyTokenObtainPairSerializer (TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username

        return token


class ProfileSerializer(serializers.ModelSerializer):

    mystaff = MyStaffSerializer(write_only=True)

    class Meta:
        model = MyUser
        fields = ["username", "is_staff", "mystaff"]
        depth = 2
        read_only_fields = ["username"]

    def to_internal_value(self, data):
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

