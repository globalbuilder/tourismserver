# apps/attractions/serializers.py

from rest_framework import serializers
from .models import Category, Attraction, Feedback, Favorite

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'image',
            'price',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ('created_at', 'updated_at')


class AttractionSerializer(serializers.ModelSerializer):
    # If you want to show category data, you can do nested read-only:
    category_name = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = Attraction
        fields = [
            'id',
            'category',
            'category_name',
            'name',
            'latitude',
            'longitude',
            'address',
            'description',
            'image',
            'average_rating',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ('average_rating', 'created_at', 'updated_at')


class FeedbackSerializer(serializers.ModelSerializer):
    # For convenience, display the user's username and attraction name
    user_username = serializers.ReadOnlyField(source='user.username')
    attraction_name = serializers.ReadOnlyField(source='attraction.name')

    class Meta:
        model = Feedback
        fields = [
            'id',
            'user',
            'attraction',
            'rating',
            'comment',
            'created_at',
            'user_username',
            'attraction_name'
        ]
        read_only_fields = ('created_at',)


class FavoriteSerializer(serializers.ModelSerializer):
    user_username = serializers.ReadOnlyField(source='user.username')
    attraction_name = serializers.ReadOnlyField(source='attraction.name')

    class Meta:
        model = Favorite
        fields = [
            'id',
            'user',
            'attraction',
            'created_at',
            'user_username',
            'attraction_name'
        ]
        read_only_fields = ('created_at',)
