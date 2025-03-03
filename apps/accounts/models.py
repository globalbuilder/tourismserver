# apps/accounts/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    """
    A custom user model extending Django's AbstractUser.
    
    Fields inherited from AbstractUser:
      - username, password, email, first_name, last_name, is_staff,
        is_superuser, is_active, date_joined, etc.

    Additional fields below:
      - phone_number
      - is_verified
      - created_at
    """

    phone_number = models.CharField(max_length=20, blank=True, null=True)
    is_verified = models.BooleanField(default=False)  # For e.g. verifying email or phone
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        # Return email if present, otherwise fallback to username
        return self.email if self.email else self.username


class Profile(models.Model):
    """
    Profile holds additional personal data for each user.
    One-to-one with the custom User model.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    
    # Optional demographic data
    date_of_birth = models.DateField(blank=True, null=True)
    image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    biography = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"Profile of {self.user.username}"
