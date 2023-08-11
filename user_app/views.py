from rest_framework import status
from rest_framework.generics import RetrieveAPIView, CreateAPIView, UpdateAPIView
from rest_framework.response import Response
from .models import MyUser, MyStaff
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
import logging
from .serializers import RegisterSerializer, ProfileSerializer, MyTokenRefreshSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .permissions import IsAdmin, IsUser

logger = logging.getLogger(__name__)

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


class ProfileViewset(RetrieveAPIView, UpdateAPIView):
    queryset = MyUser.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = "username"
    permission_classes = [IsAdmin | IsUser]

class MyTokenObtainPairView(TokenObtainPairView):

    def finalize_response(self, request, response, *args, **kwargs):

        new_response = super().finalize_response(request, response, *args, **kwargs)

        if response.data.get('access'):
            user = MyUser.objects.get(username=request.data['username'])
            
            # Return username
            new_response.data['username'] = user.username

        # Return the refresh token as a http-only cookie - token can be stored as sessionStorage

        if response.data.get('refresh'):
            refresh_lifetime = 60 * 60 * 24 # Set expiry datetime of refresh cookie to 15 days
            new_response.set_cookie('refresh', 
                response.data['refresh'], 
                max_age=refresh_lifetime, 
                httponly=True, 
                secure=True,
                samesite="Lax",
                domain="https://127.0.0.1:3000/"
            )
            del new_response.data['refresh']
    
        return new_response


class MyTokenRefreshView(TokenRefreshView):
    serializer_class = MyTokenRefreshSerializer

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    
    
