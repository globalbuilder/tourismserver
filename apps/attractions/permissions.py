# apps/attractions/permissions.py
from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    For Feedback/Favorite: user can read any, but only the owner can update/delete.
    """
    def has_object_permission(self, request, view, obj):
        # Safe methods = GET, HEAD, OPTIONS
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user
