"""Authentication Serializer module file"""
import os

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client

from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from dj_rest_auth.registration.views import SocialLoginView

from . import google
from ..models import Users
from .register import register_social_user


class RegistrationSerializer(serializers.ModelSerializer):
    """User Registration Serializer"""
    password = serializers.CharField(write_only=True)

    class Meta:
        """Pre display all fields except password field since it is write only"""
        model = Users
        fields = [
            "id",
            "username",
            "Email_Address",
            "password",
            "is_active",
            "is_staff"
        ]


class LoginSerializer(serializers.ModelSerializer):
    """User and Admin Login module serializer class"""
    password = serializers.CharField(write_only=True)

    class Meta:
        """Fields to serialize for user to view except ofcourse password"""
        model = Users
        fields = ("username", "Email_Address", "password", "token")
        read_only_fields = ["token"]


class ChangePasswordSerializer(serializers.ModelSerializer):
    """User change password serializer"""
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    class Meta:
        """Pre displayed fields for user"""
        model = Users
        fields = [
            "username",
            "Email_Address",
            "old_password",
            "new_password"
        ]


class GoogleSocialAuthSerializer(serializers.Serializer):
    """Google Sign up serializer for users."""
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = google.Google.validate(auth_token)
        try:
            user_data['sub']
        except:
            raise serializers.ValidationError(
                'The token is invalid or expired. Please login again.')
        email = user_data['email']
        name = user_data['name']
        return register_social_user(
            email=email, username=name)
