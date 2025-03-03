# apps/attractions/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet,
    AttractionViewSet,
    FeedbackViewSet,
    FavoriteViewSet
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'attractions', AttractionViewSet, basename='attractions')
router.register(r'feedback', FeedbackViewSet, basename='feedback')
router.register(r'favorites', FavoriteViewSet, basename='favorites')

urlpatterns = [
    path('', include(router.urls)),
]
