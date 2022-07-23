"""Authentication Serializer module file"""
from authentications.api import google
from authentications.api.register import register_social_user
from authentications.models import Users
from django.forms import ValidationError
from httplib2 import Response
from rest_framework import serializers


class RegistrationSerializer(serializers.ModelSerializer):
    """User Registration Serializer"""
    class Meta:
        """Pre display all fields except password field since it is write only"""
        model = Users
        fields = [
            "id",
            "username",
            "email_address",
            'password'
        ]
class AdminUpdateSerializer(serializers.ModelSerializer):
    """User Registration Serializer"""

    class Meta:
        """Pre display all fields except password field since it is write only"""
        model = Users
        fields = [
            "id",
            "username",
            "email_address",
            "is_active",
            "is_superuser"
        ]
class AdminUpdateDetailSerializer(serializers.ModelSerializer):
    """User Registration Serializer"""

    class Meta:
        """Pre display all fields except password field since it is write only"""
        model = Users
        fields = [
            "is_active",
        ]
class LibarianRegistrationSerializer(serializers.ModelSerializer):
    """Libarian Registration Serializer"""

    class Meta:
        """Pre display all fields except password field since it is write only"""
        model = Users
        fields = [
            "id",
            "username",
            "email_address",
        ]



class LoginSerializer(serializers.ModelSerializer):
    """User and Admin Login module serializer class"""
    password = serializers.CharField(write_only=True)

    class Meta:
        """Fields to serialize for user to view except ofcourse password"""
        model = Users
        fields = ("email_address", "password")
        read_only_fields = ["token"]


class ChangePasswordSerializer(serializers.ModelSerializer):
    """User change password serializer"""
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    class Meta:
        """Pre displayed fields for user"""
        model = Users
        fields = [
            "old_password",
            "new_password"
        ]


class GoogleSocialAuthSerializer(serializers.Serializer):
    """Google Sign up serializer for users."""
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        """Validating the auth token"""
        user_data = google.Google.validate(auth_token)
        try:
            user_data['sub']
        except ValidationError:
            return Response({
                "status":"failure",
                "details":"Token expired"
            })
        except ValueError:
            return Response({
                "status":"failure",
                "details":"Token expired"
            })
        email = user_data['email']
        name = user_data['name']
        return register_social_user(
            email=email, username=name)
