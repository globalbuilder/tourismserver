# apps/attractions/views.py

from rest_framework import viewsets, permissions, status, filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import Category, Attraction, Feedback, Favorite
from .serializers import (
    CategorySerializer, 
    AttractionSerializer, 
    FeedbackSerializer, 
    FavoriteSerializer
)
from .permissions import IsFeedbackOwnerOrSuperuser
from notifications.models import Notification


class CategoryViewSet(viewsets.ModelViewSet):
    """
    Manage categories (e.g., 'Museum', 'Park', etc.).
    Only authenticated users can see them by default.
    If you want them publicly visible (no login needed),
    replace permissions.IsAuthenticated with permissions.AllowAny.
    
    Includes:
      - Filtering by 'name'
      - Searching by 'name'
    """
    queryset = Category.objects.all().order_by('-created_at')
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    # DRF filtering & searching
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['name']   # e.g., GET /categories/?name=Museum
    search_fields = ['name']      # e.g., GET /categories/?search=Muse


class AttractionViewSet(viewsets.ModelViewSet):
    """
    Manage attractions linked to a Category.
    Only superusers can create, update, or delete attractions;
    normal users can read them.

    Includes:
      - Filter by 'category' or 'average_rating'
      - Search by 'name', 'address', or 'description'
    """
    queryset = Attraction.objects.all().order_by('-created_at')
    serializer_class = AttractionSerializer
    permission_classes = [permissions.IsAuthenticated]

    # DRF filtering & searching
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category', 'average_rating']
    search_fields = ['name', 'address', 'description']

    def perform_create(self, serializer):
        """Only superuser can create."""
        if not self.request.user.is_superuser:
            return Response(
                {"detail": "Only admin can create attractions."},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer.save()
        Notification.objects.create(
            user=None,
            title="New Attraction Added",
            message=f"Check out the newly added attraction: {Attraction.name}!",
            created_by=self.request.user
        )

    def perform_update(self, serializer):
        """Only superuser can update."""
        if not self.request.user.is_superuser:
            return Response(
                {"detail": "Only admin can edit attractions."},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer.save()

    def perform_destroy(self, instance):
        """Only superuser can delete."""
        if not self.request.user.is_superuser:
            return Response(
                {"detail": "Only admin can delete attractions."},
                status=status.HTTP_403_FORBIDDEN
            )
        instance.delete()


class FeedbackViewSet(viewsets.ModelViewSet):
    """
    Manage feedback (ratings/comments) on an attraction.
    - Only the feedback owner or a superuser can edit/delete.
    - Normal user sees only their own feedback; superuser sees all.

    Includes:
      - Filter by 'attraction' or 'rating'
      - Search by 'comment'
    """
    queryset = Feedback.objects.all().order_by('-created_at')
    serializer_class = FeedbackSerializer
    permission_classes = [permissions.IsAuthenticated, IsFeedbackOwnerOrSuperuser]

    # DRF filtering & searching
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['attraction', 'rating']
    search_fields = ['comment']

    def get_queryset(self):
        """Restrict normal users to their own feedback; superusers see all."""
        if self.request.user.is_superuser:
            return Feedback.objects.all().order_by('-created_at')
        return Feedback.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        """
        Auto-assign current user as feedback owner.
        """
        serializer.save(user=self.request.user)


class FavoriteViewSet(viewsets.ModelViewSet):
    """
    Manage favorites: which user favorited which attraction.
    - Normal user sees only their favorites; superuser sees all.

    Includes:
      - Filter by 'attraction'
      - Search by 'attraction__name'
    """
    queryset = Favorite.objects.all().order_by('-created_at')
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    # DRF filtering & searching
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['attraction']        # GET /favorites/?attraction=5
    search_fields = ['attraction__name']     # GET /favorites/?search=Museum

    def get_queryset(self):
        """Restrict normal users to their own favorites; superuser sees all."""
        if self.request.user.is_superuser:
            return Favorite.objects.all().order_by('-created_at')
        return Favorite.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        """Link the created Favorite to the current user."""
        serializer.save(user=self.request.user)
