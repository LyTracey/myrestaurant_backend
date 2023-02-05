from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.contrib.auth import get_user_model
import logging

logger = logging.getLogger(__name__)
User = get_user_model()
logger.info(User)

class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

class Staff(BasePermission):
    def has_permission(self, request, view):
        if request.user:
            u = User.objects.get(id=request.user.pk)
            if u.is_staff:
                return True
        return False