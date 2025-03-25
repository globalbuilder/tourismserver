# apps/notifications/views.py

from rest_framework import viewsets, permissions
from rest_framework.response import Response
from django.db.models import Q
from .models import Notification
from .serializers import NotificationSerializer

class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Provides read-only access to notifications.
    Normal users see only notifications addressed to them or broadcast.
    When a user retrieves a single notification, it is automatically marked as read.
    """
    queryset = Notification.objects.all().order_by('-created_at')
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Notification.objects.all().order_by('-created_at')
        return Notification.objects.filter(
            Q(user=self.request.user) | Q(user__isnull=True)
        ).order_by('-created_at')

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Automatically mark as read if not already
        if not instance.is_read:
            instance.is_read = True
            instance.save(update_fields=['is_read'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
