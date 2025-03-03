# apps/notifications/models.py

from django.db import models
from django.utils import timezone
from accounts.models import User

class Notification(models.Model):
    """
    Stores notifications in the system. A notification can be directed
    to a specific user (user_id) or be broadcast (user = null).
    'created_by' is the user who generated the notification, or null if system-generated.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='notifications',
        help_text="The user who will receive the notification (null for broadcast)."
    )
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='created_notifications',
        help_text="The user who created the notification, null if system-generated."
    )
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        if self.user:
            return f"Notification to {self.user.username} - {self.title}"
        return f"Broadcast Notification - {self.title}"
