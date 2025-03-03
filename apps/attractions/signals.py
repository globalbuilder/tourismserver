# apps/attractions/signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Avg
from .models import Feedback, Attraction

@receiver([post_save, post_delete], sender=Feedback)
def update_attraction_average_rating(sender, instance, **kwargs):
    attraction = instance.attraction
    feedback_qs = attraction.feedbacks.all()
    new_avg = feedback_qs.aggregate(Avg('rating'))['rating__avg'] or 0.0
    attraction.average_rating = new_avg
    attraction.save()
