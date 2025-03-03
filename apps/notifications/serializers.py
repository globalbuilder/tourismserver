# apps/notifications/serializers.py

from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    user_username = serializers.ReadOnlyField(source='user.username')
    created_by_username = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = Notification
        fields = [
            'id',
            'user',
            'title',
            'message',
            'is_read',
            'created_by',
            'created_at',
            'user_username',
            'created_by_username'
        ]
        read_only_fields = ('created_at',)
