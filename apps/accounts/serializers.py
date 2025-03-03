# apps/accounts/serializers.py

from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """
    Handles creation and updating of the custom User object,
    including secure password hashing.
    """
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'password',
            'first_name',
            'last_name',
            'phone_number',
            'is_verified',
            'is_staff',
            'is_superuser',
            'is_active',
            'created_at',
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'created_at': {'read_only': True},
            'is_superuser': {'read_only': True},  # Typically only changed in admin
            'is_staff': {'read_only': True},      # Typically only changed in admin
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.password = make_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.password = make_password(password)
        instance.save()
        return instance


class ProfileSerializer(serializers.ModelSerializer):
    """
    Profile details for each user, typically read or updated by the user themselves.
    """
    user_id = serializers.ReadOnlyField(source='user.id')
    username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Profile
        fields = [
            'user_id',
            'username',
            'date_of_birth',
            'image',
            'address',
            'biography',
            'website',
        ]
        read_only_fields = ('user_id', 'username')
