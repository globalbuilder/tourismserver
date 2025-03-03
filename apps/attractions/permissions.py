# apps/attractions/permissions.py

from rest_framework import permissions

class IsFeedbackOwnerOrSuperuser(permissions.BasePermission):
    """
    Grants access if the request user is either the owner of the Feedback
    or a superuser.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        # Allow if user is superuser
        if request.user.is_superuser:
            return True
        # Otherwise, only the feedback's owner can modify
        return obj.user == request.user
