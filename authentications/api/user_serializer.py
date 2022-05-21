from ..models import Users

from rest_framework import serializers


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)

    class Meta:
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
    password = serializers.CharField(write_only = True)
    class Meta:
        model= Users
        fields = ("username","Email_Address","password","token")
        read_only_fields = ["token"]


class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(required= True)
    new_password = serializers.CharField(required = True)
    class Meta:
        model = Users
        fields = [
            "username",
            "Email_Address",
            "old_password",
            "new_password"
        ]
