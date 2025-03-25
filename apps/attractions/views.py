# apps/attractions/views.py

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from .models import Category, Attraction, Feedback, Favorite
from .serializers import (
    CategorySerializer, AttractionSerializer,
    FeedbackSerializer, FavoriteSerializer
)
from .permissions import IsOwnerOrReadOnly

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Normal user can only list/retrieve categories.
    """
    queryset = Category.objects.all().order_by('-created_at')
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    # Optional filters/search
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['name']


class AttractionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Normal user can only list/retrieve attractions.
    """
    queryset = Attraction.objects.all().order_by('-created_at')
    serializer_class = AttractionSerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['category']
    search_fields = ['name', 'address', 'description']


class FeedbackViewSet(viewsets.ModelViewSet):
    """
    Normal user can create, view, update, or delete their own feedback.
    """
    queryset = Feedback.objects.all().order_by('-created_at')
    serializer_class = FeedbackSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        # Assign the feedback to the current user
        serializer.save(user=self.request.user)

    def get_queryset(self):
        """
        If you want each user only to see their own feedback, do:
        """
        if self.request.user.is_superuser:
            return Feedback.objects.all().order_by('-created_at')
        return Feedback.objects.filter(user=self.request.user).order_by('-created_at')


class FavoriteViewSet(viewsets.ModelViewSet):
    """
    Normal user can create, view, update, or delete their own favorite attractions.
    """
    queryset = Favorite.objects.all().order_by('-created_at')
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        """
        If you want each user only to see their own favorites.
        """
        if self.request.user.is_superuser:
            return Favorite.objects.all().order_by('-created_at')
        return Favorite.objects.filter(user=self.request.user).order_by('-created_at')
