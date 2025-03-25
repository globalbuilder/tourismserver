# accounts/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    """
    Custom User model:
      - Inherits from AbstractUser (username, email, password, etc.)
      - Adds is_verified, created_at
      - phone_number removed (moved to Profile)
    """
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return self.email if self.email else self.username


class Profile(models.Model):
    """
    Profile: one-to-one with the custom User model.
    Now includes phone_number for contact info.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    date_of_birth = models.DateField(blank=True, null=True)
    image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    biography = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"Profile of {self.user.username}"
