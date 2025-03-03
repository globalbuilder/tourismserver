# apps/accounts/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Admin for managing the custom User model via Django's built-in UserAdmin.
    """
    list_display = (
        'id', 'username', 'email', 'phone_number',
        'is_verified', 'is_staff', 'is_superuser', 'is_active'
    )
    list_filter = ('is_verified', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email', 'phone_number')
    ordering = ('-created_at',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('email', 'phone_number')}),
        ('Permissions', {
            'fields': (
                'is_verified',
                'is_staff', 'is_superuser', 'is_active',
                'groups', 'user_permissions'
            )
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined', 'created_at')}),
    )
    readonly_fields = ('created_at', 'date_joined', 'last_login')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    Admin for managing user profiles.
    """
    list_display = ('user', 'date_of_birth', 'address', 'website')
    search_fields = ('user__username', 'user__email', 'address', 'biography')
