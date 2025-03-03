# apps/attractions/admin.py

from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Attraction, Feedback, Favorite

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'image_preview', 'created_at', 'updated_at')
    search_fields = ('name',)
    readonly_fields = ('created_at', 'updated_at')

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit:cover;"/>', obj.image.url)
        return "No Image"
    image_preview.short_description = "Image Preview"

@admin.register(Attraction)
class AttractionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'average_rating', 'image_preview', 'price', 'created_at', 'updated_at')
    list_filter = ('category',)
    search_fields = ('name', 'address')
    readonly_fields = ('created_at', 'updated_at', 'average_rating')

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit:cover;"/>', obj.image.url)
        return "No Image"
    image_preview.short_description = "Image Preview"

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'attraction', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user__username', 'attraction__name')

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'attraction', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'attraction__name')
