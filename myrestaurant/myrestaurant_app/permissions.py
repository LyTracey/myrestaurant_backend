from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.contrib.auth.models import User, Group
import logging

logger = logging.getLogger(__name__)

class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

class StaffAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user:
            u = User.objects.get(id=request.user.pk)
            groups = [group_name for _, group_name in u.groups.values_list()]
            if "admin" in groups:
                return True
        return False