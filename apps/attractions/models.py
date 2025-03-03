# apps/attractions/models.py

from django.db import models
from django.utils import timezone
from accounts.models import User
from decimal import Decimal

class Category(models.Model):
    """
    Represents an attraction category (e.g., Museum, Park, etc.).
    """
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='categories/', null=True, blank=True)

    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Attraction(models.Model):
    """
    Represents a specific tourist attraction. Linked to a Category.
    """
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='attractions')
    name = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    address = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='attractions/', blank=True, null=True)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00')
    )

    average_rating = models.FloatField(default=0.0)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.category.name})"


class Feedback(models.Model):
    """
    Stores user feedback (rating + comment) for an Attraction.
    The average rating is stored in Attraction.average_rating and recalculated
    via signals whenever Feedback changes.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedbacks')
    attraction = models.ForeignKey(Attraction, on_delete=models.CASCADE, related_name='feedbacks')
    rating = models.PositiveIntegerField()
    comment = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return f"Feedback {self.pk} by {self.user.username} -> {self.attraction.name}"


class Favorite(models.Model):
    """
    Many-to-many relationship between User and Attraction.
    A user can 'favorite' multiple attractions.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    attraction = models.ForeignKey(Attraction, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return f"{self.user.username} favorited {self.attraction.name}"
