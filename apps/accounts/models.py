from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    """
    Custom User model:
      - Inherits from AbstractUser (username, password, etc.)
      - Email is no longer stored here (moved to Profile)
      - Adds is_verified and created_at
    """
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return self.username  # email not available here

class Profile(models.Model):
    """
    Profile: one-to-one with the custom User model.
    Now includes email and phone_number for contact info.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    date_of_birth = models.DateField(blank=True, null=True)
    image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    biography = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"Profile of {self.user.username}"
