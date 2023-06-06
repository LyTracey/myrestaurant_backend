from rest_framework.permissions import BasePermission
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
import logging

logger = logging.getLogger(__name__)
User = get_user_model()

class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        if isinstance(request.user, AnonymousUser):
            return False
        if (request.user.is_admin):
            return True
        return False

class IsUser(BasePermission):

    def has_permission(self, request, view):
        if isinstance(request.user, AnonymousUser):
            return False
        return True

    def has_object_permission(self, request, view, obj):
        if isinstance(request.user, AnonymousUser):
            return False
        return obj.username == request.user.username