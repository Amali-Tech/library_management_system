"""Authentication Serializer module file"""
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client

from rest_framework import serializers

from dj_rest_auth.registration.views import SocialLoginView


from ..models import Users


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


class GoogleLogin(SocialLoginView):
    """Google Sign up serializer for users."""
    authentication_classes = []
    adapter_class = GoogleOAuth2Adapter
    callback_url = "http://127.0.0.1:8000"
    client_class = OAuth2Client
