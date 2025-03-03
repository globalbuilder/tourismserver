# apps/notifications/views.py

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer
from django.db.models import Q

class NotificationViewSet(viewsets.ModelViewSet):
    """
    Provides CRUD for Notification model.
    By default, only authenticated users can access.
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

    def perform_create(self, serializer):
        # Restrict creation to superusers only
        if not self.request.user.is_superuser:
            return Response(
                {"detail": "Only superusers can create notifications."},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer.save(created_by=self.request.user)

    def partial_update(self, request, *args, **kwargs):
        """
        If you want a custom endpoint for 'mark_as_read', you could do:
        PATCH /api/notifications/<pk>/ { "is_read": true }
        """
        return super().partial_update(request, *args, **kwargs)
