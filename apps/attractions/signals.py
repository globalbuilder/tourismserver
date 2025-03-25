# apps/attractions/signals.py

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Avg
from .models import Feedback, Attraction

@receiver([post_save, post_delete], sender=Feedback)
def update_attraction_average_rating(sender, instance, **kwargs):
    attraction = instance.attraction
    qs = attraction.feedbacks.all()
    if qs.exists():
        attraction.average_rating = qs.aggregate(Avg('rating'))['rating__avg']
    else:
        attraction.average_rating = 0.0
    attraction.save()
