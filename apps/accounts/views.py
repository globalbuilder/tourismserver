# accounts/views.py

from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import (
    RegisterSerializer, UserSerializer, ProfileSerializer,
    ChangePasswordSerializer
)
from .models import Profile
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    """
    POST /api/accounts/register/
    Body: { first_name, last_name, username, password1, password2, image(optional) }
    Creates User + Profile. Returns 201 with user data.
    """
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class UserDetailUpdateView(generics.RetrieveUpdateAPIView):
    """
    GET/PUT/PATCH /api/accounts/user/
    The current user can edit first_name, last_name, email, etc.
    (cannot change password here).
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class ProfileDetailUpdateView(generics.RetrieveUpdateAPIView):
    """
    GET/PUT/PATCH /api/accounts/profile/
    The current user's profile, including phone_number, image, etc.
    """
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return Profile.objects.get(user=self.request.user)


class ChangePasswordView(generics.UpdateAPIView):
    """
    POST or PATCH to /api/accounts/change-password/
    Body: { old_password, new_password1, new_password2 }
    """
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        user.set_password(serializer.validated_data['new_password1'])
        user.save()
        return Response({"detail": "Password updated successfully."}, status=status.HTTP_200_OK)


class LogoutView(APIView):
    """
    POST /api/accounts/logout/
    Body: { "refresh": "<refresh_token>" }
    Blacklist the refresh token if using SimpleJWT token blacklisting.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Logged out."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
