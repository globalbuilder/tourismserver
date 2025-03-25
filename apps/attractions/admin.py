# apps/attractions/admin.py

from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Attraction, Feedback, Favorite

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'image_preview', 'created_at', 'updated_at')
    search_fields = ('name',)
    ordering = ('id',)

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width:50px; height:50px; object-fit:cover;" />',
                obj.image.url
            )
        return "No Image"
    image_preview.short_description = "Category Image"


@admin.register(Attraction)
class AttractionAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'category', 'average_rating',
        'image_preview', 'created_at', 'updated_at'
    )
    search_fields = ('name', 'address')
    list_filter = ('category',)
    ordering = ('id',)

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width:50px; height:50px; object-fit:cover;" />',
                obj.image.url
            )
        return "No Image"
    image_preview.short_description = "Attraction Image"


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'attraction', 'rating', 'created_at')
    search_fields = ('user__username', 'attraction__name', 'comment')
    ordering = ('-created_at',)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'attraction', 'created_at')
    search_fields = ('user__username', 'attraction__name')
    ordering = ('-created_at',)
