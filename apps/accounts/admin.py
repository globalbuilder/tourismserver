# accounts/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import User, Profile

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Custom admin for your User model.
    Inherits from UserAdmin, so it already handles fields like 'username', 'email', 'is_staff', etc.
    We add 'is_verified' and 'created_at', plus ordering & filtering.
    """
    list_display = (
        'id', 'username', 'email','first_name', 'last_name', 'is_verified',
        'is_staff', 'is_superuser', 'is_active', 'created_at'
    )
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'is_verified')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('id',)

    # Show certain fields in the form; you can customize more if needed
    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Personal Info', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Extra Info', {
            'fields': ('is_verified', 'created_at')
        }),
        ('Permissions', {
            'fields': (
                'is_staff', 'is_superuser', 'is_active',
                'groups', 'user_permissions'
            )
        }),
    )
    readonly_fields = ('created_at', 'date_joined', 'last_login')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    Admin for Profile, displaying phone_number, image thumbnail, etc.
    """
    list_display = ('user', 'phone_number', 'image_preview', 'date_of_birth')
    search_fields = ('user__username', 'user__email', 'phone_number')
    list_filter = ('date_of_birth',)
    ordering = ('user',)

    def image_preview(self, obj):
        """
        Show a small thumbnail in the admin list if the profile has an image.
        """
        if obj.image:
            return format_html(
                '<img src="{}" style="width:50px; height:50px; object-fit:cover;" />',
                obj.image.url
            )
        return "No Image"
    image_preview.short_description = "Profile Image"
