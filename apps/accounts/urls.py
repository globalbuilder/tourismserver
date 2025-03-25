# accounts/urls.py

from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (
    RegisterView, UserDetailUpdateView, ProfileDetailUpdateView,
    ChangePasswordView, LogoutView
)

urlpatterns = [
    # Registration, login, logout
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # User info & Profile
    path('user/', UserDetailUpdateView.as_view(), name='user_detail_update'),
    path('profile/', ProfileDetailUpdateView.as_view(), name='profile_detail_update'),

    # Change Password
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
]
