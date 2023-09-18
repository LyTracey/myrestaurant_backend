from rest_framework import status
from rest_framework.generics import RetrieveAPIView, CreateAPIView, UpdateAPIView
from rest_framework.response import Response
from .models import MyUser, MyStaff
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
import logging
from .serializers import RegisterSerializer, ProfileSerializer, MyTokenObtainPairSerializer
from .permissions import IsAdmin, IsUser
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken

logger = logging.getLogger(__name__)

# Override authentication method to prevent authentication for public pages
class JWTAuthenticationSafe(JWTAuthentication):
    def authenticate(self, request):
        try:
            return super().authenticate(request=request)
        except InvalidToken:
            return None

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def user_handler(sender, instance, **kwargs):
    exists = MyStaff.objects.filter(user_id=instance.id).exists()
    if not exists and instance.is_staff:
        user = MyStaff(user=instance)
        user.save()
        return Response({'message': "User created in MyStaff model"}, status=status.HTTP_201_CREATED)
    elif exists and not instance.is_staff:
        MyStaff.objects.get(user_id=instance.id).delete()
        return Response({'message': "User deleted from MyStaff model"})
    return Response({'message': "User updated."})


class RegisterViewset(CreateAPIView):
    queryset = MyUser.objects.all()
    serializer_class = RegisterSerializer
    authentication_classes = []
    permission_classes = []


class ProfileViewset(RetrieveAPIView, UpdateAPIView):
    queryset = MyUser.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = "username"
    permission_classes = [IsAdmin | IsUser]



class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
