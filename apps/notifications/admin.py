# apps/notifications/admin.py

from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'title', 'user', 'is_read', 'created_by', 'created_at'
    )
    list_filter = ('is_read', 'created_at')
    search_fields = ('title', 'message', 'user__username', 'created_by__username')
    readonly_fields = ('created_at',)
