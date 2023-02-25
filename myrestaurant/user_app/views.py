from rest_framework import status
from rest_framework.response import Response
from .models import MyUser, MyStaff
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
import logging
from rest_framework.viewsets import ModelViewSet
from .serializers import MyUserSerializer

logger = logging.getLogger(__name__)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def user_handler(sender, instance, **kwargs):
    exists = MyStaff.objects.filter(staff_id=instance.id).exists()
    if not exists and instance.is_staff:
        user = MyStaff(staff_id=instance.id)
        user.save()
        return Response({'message': "User created in MyStaff model"}, status=status.HTTP_201_CREATED)
    elif exists and not instance.is_staff:
        MyStaff.objects.get(staff_id=instance.id).delete()
        return Response({'message': "User deleted from MyStaff model"})
    return Response({'message': "User updated."})


class MyUserViewset(ModelViewSet):
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer