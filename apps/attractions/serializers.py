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
            'created_at',
            'updated_at'
        ]
        read_only_fields = ('created_at', 'updated_at')


class AttractionSerializer(serializers.ModelSerializer):
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
            'price',
            'average_rating',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ('average_rating', 'created_at', 'updated_at')


class FeedbackSerializer(serializers.ModelSerializer):
    # user info read-only
    user_username = serializers.ReadOnlyField(source='user.username')
    attraction_name = serializers.ReadOnlyField(source='attraction.name')

    class Meta:
        model = Feedback
        fields = [
            'id',
            'user',
            'user_username',
            'attraction',
            'attraction_name',
            'rating',
            'comment',
            'created_at'
        ]
        read_only_fields = ('user', 'created_at')


class FavoriteSerializer(serializers.ModelSerializer):
    user_username = serializers.ReadOnlyField(source='user.username')
    attraction_name = serializers.ReadOnlyField(source='attraction.name')

    class Meta:
        model = Favorite
        fields = [
            'id',
            'user',
            'user_username',
            'attraction',
            'attraction_name',
            'created_at'
        ]
        read_only_fields = ('user', 'created_at')
