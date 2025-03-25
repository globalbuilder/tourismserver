# accounts/serializers.py

from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from .models import Profile

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    """
    Register with:
      - first_name, last_name, username
      - password1, password2
      - image (optional)
    Creates a User + Profile
    """
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    image = serializers.ImageField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username',
                  'password1', 'password2', 'image']

    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return attrs

    def create(self, validated_data):
        password1 = validated_data.pop('password1')
        validated_data.pop('password2')  # not needed anymore
        image = validated_data.pop('image', None)

        user = User(**validated_data)
        user.set_password(password1)
        user.save()
        # create or update profile
        if image:
            Profile.objects.create(user=user, image=image)
        else:
            Profile.objects.create(user=user)
        return user


class UserSerializer(serializers.ModelSerializer):
    """
    For reading/updating user fields (not password).
    - 'id', 'username' read-only
    """
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email',
            'first_name', 'last_name',
            'is_verified', 'created_at'
        ]
        read_only_fields = ['id', 'username', 'is_verified', 'created_at']


class ProfileSerializer(serializers.ModelSerializer):
    """
    For reading/updating profile fields, including phone_number.
    """
    class Meta:
        model = Profile
        fields = [
            'user_id', 'phone_number', 'date_of_birth',
            'image', 'address', 'biography', 'website'
        ]
        read_only_fields = ['user_id']


class ChangePasswordSerializer(serializers.Serializer):
    """
    For changing password.
    old_password + new_password1 + new_password2
    """
    old_password = serializers.CharField(write_only=True)
    new_password1 = serializers.CharField(write_only=True)
    new_password2 = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs['new_password1'] != attrs['new_password2']:
            raise serializers.ValidationError("New passwords do not match.")
        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not check_password(value, user.password):
            raise serializers.ValidationError("Old password is incorrect.")
        return value
