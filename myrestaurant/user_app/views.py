from rest_framework import status
from rest_framework.generics import RetrieveAPIView, CreateAPIView, UpdateAPIView
from rest_framework.response import Response
from .models import MyUser, MyStaff
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
import logging
from .serializers import RegisterSerializer, ProfileSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import AnonymousUser

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


class RegisterViewset(CreateAPIView, UpdateAPIView):
    queryset = MyUser.objects.all()
    serializer_class = RegisterSerializer


class ProfileViewset(RetrieveAPIView):
    queryset = MyUser.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = "username"

class TokenView(TokenObtainPairView):
    def finalize_response(self, request, response, *args, **kwargs):
        if not isinstance(request.user, AnonymousUser):
            # Return is_staff
            user = MyUser.objects.filter(username=request.data['username']).first()
            response.data['isStaff'] = user.is_staff

        # Return the refresh token as a http-only cookie - token can be stored as sessionStorage
        if response.data.get('refresh'):
            lifetime = 3600 * 24
            response.set_cookie('refresh', response.data['refresh'], max_age=lifetime, httponly=True)
            del response.data['refresh']
        

        return super().finalize_response(request, response, *args, **kwargs)
