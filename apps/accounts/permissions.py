# apps/accounts/permissions.py
from rest_framework import permissions

class IsProfileOwnerOrSuperuser(permissions.BasePermission):
    """
    Allows access only if the requesting user is either a superuser
    or the same user who owns the profile.
    """

    def has_object_permission(self, request, view, obj):
        # Check if the user is superuser
        if request.user.is_superuser:
            return True

        # Otherwise, ensure the object's user is the requesting user
        return obj.user == request.user
