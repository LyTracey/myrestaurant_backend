from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
import logging

logger = logging.getLogger(__name__)
User = get_user_model()

class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

class Staff(BasePermission):
    def has_permission(self, request, view):
        if isinstance(request.user, AnonymousUser):
            return False
        return request.user.is_staff

class Chef(BasePermission):
    def has_permission(self, request, view):
        if isinstance(request.user, AnonymousUser):
            return False
        return request.user.mystaff.role == "CHEF"
    
class Sales(BasePermission):
    def has_permission(self, request, view):
        if isinstance(request.user, AnonymousUser):
            return False
        return request.user.mystaff.role == "SALES"

class Manager(BasePermission):
    def has_permission(self, request, view):
        if isinstance(request.user, AnonymousUser):
            return False
        return request.user.mystaff.role == "MANAGER"