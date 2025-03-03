# apps/accounts/views.py

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import Profile
from .serializers import UserSerializer, ProfileSerializer
from .permissions import IsProfileOwnerOrSuperuser

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    """
    CRUD for User. Only authenticated users can view their own detail.
    Superuser can view everyone's. 
    """
    queryset = User.objects.all().order_by('-created_at')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        """
        If the user is superuser, return all users.
        Otherwise, return only their own user object.
        """
        if request.user.is_superuser:
            return super().list(request, *args, **kwargs)
        self.queryset = User.objects.filter(id=request.user.id)
        return super().list(request, *args, **kwargs)


class ProfileViewSet(viewsets.ModelViewSet):
    """
    Each user has one Profile. Access restricted by IsProfileOwnerOrSuperuser.
    """
    queryset = Profile.objects.select_related('user').all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsProfileOwnerOrSuperuser]

    def get_queryset(self):
        """
        Superuser sees all, normal user sees only their own profile.
        """
        if self.request.user.is_superuser:
            return Profile.objects.select_related('user').all()
        return Profile.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        A user can create their own profile only if they don't have one.
        """
        user = self.request.user
        if Profile.objects.filter(user=user).exists():
            return Response({"detail": "Profile already exists."},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer.save(user=user)
