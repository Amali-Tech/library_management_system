"""Authentication views for users and admin"""
import string
import random

from django.contrib.auth import authenticate

from rest_framework.authentication import BasicAuthentication
from rest_framework.generics import GenericAPIView, UpdateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from authentications.models import Users
from authentications.api.user_serializer import LoginSerializer, RegistrationSerializer, AdminUpdateSerializer,ChangePasswordSerializer, GoogleSocialAuthSerializer, LibarianRegistrationSerializer


class IsSuperUser(IsAdminUser):
    """Checking to see if the current user is Admin user authentication"""

    def has_permission(self, request, view):
        """When called, gives the user permissions to some views"""
        return bool(request.user and request.user.is_superuser)


class AuthUserAPIView(GenericAPIView):
    """When user logs in with a token, their identity can be determines"""
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """Getting the current logged in user info"""
        user = request.user
        serializer = RegistrationSerializer(user)
        return Response({"user": serializer.data})


class RegisterAPIView(GenericAPIView):
    """User register views endpoint"""
    queryset = Users.objects
    serializer_class = RegistrationSerializer
    authentication_classes = []

    def post(self, request):
        """Posting the registration details to
        be validaed by the serializer class"""
        serializers = self.serializer_class(data=request.data)
        if serializers.is_valid():
            self.queryset.create_user(**serializers.data)
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(GenericAPIView):
    """User and Admin login view endpoint"""
    queryset = Users.objects
    serializer_class = LoginSerializer
    authentication_classes = []

    def post(self, request):
        """Posting the details to be authenticated for access and token"""
        password = request.data["password"]
        username = request.data["username"]

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                serializer = self.serializer_class(user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({"message": "Account deactivated by Libarian"},
                            status=status.HTTP_401_UNAUTHORIZED)
        return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class ChangePasswordAPIView(UpdateAPIView):
    """User change password view endpoint where both users can change their password"""
    model = Users
    queryset = Users.objects
    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        """Getting the current user object to
        update the fields in the database"""
        return self.request.user

    def update(self, request, *args, **kwargs):
        """Making a PUT request to change passowrd by both user and superuser"""
        self.object = self.get_object()
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]},
                                status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response({"Status": "Success", "Message": "Password changed successfully"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LibarianRegisterListView(ListAPIView, GenericAPIView):
    """Libarian registering users view endpoint"""
    characters = list(string.ascii_letters + string.digits + "!@#$%^&*()")

    def generate_random_password(self):
        """Generate random alphanumeric passwords for new user to be changed afterwards"""
        length = 10
        random.shuffle(self.characters)
        password = []
        for _ in range(length):
            password.append(random.choice(self.characters))
        random.shuffle(password)
        return "".join(password)
    queryset = Users.objects
    serializer_class = LibarianRegistrationSerializer
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated, IsSuperUser)

    def post(self, request):
        """Post method for HTTP POST request for users to be created"""
        serializer = LibarianRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            password = self.generate_random_password()
            self.queryset.create_superuser(**serializer.data, password=password)
            return Response({"status": "success", "data": {"username": serializer.data["username"],
            "Email_Address": serializer.data["Email_Address"], "password": password}})
        return Response(serializer.errors)


class LibarianDetailView(RetrieveAPIView):
    """Superuser checking the details of other users"""
    queryset = Users.objects.all()
    serializer_class = AdminUpdateSerializer
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)

    def put(self, request, pk):
        """Put method for superuser to control user accounts"""
        queryset1 = Users.objects.get(pk=pk)
        serializer = AdminUpdateSerializer(queryset1, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

    def delete(self, reqest, pk):
        """Delete User from database API"""
        queryset1 = Users.objects.get(pk=pk)
        queryset1.delete()
        return Response({"Sucessfully Deleted": status.HTTP_204_NO_CONTENT})


class GoogleSocialAuthView(GenericAPIView):
    """Google auth view to login users from google"""
    authentication_classes = []
    permission_classes = []

    serializer_class = GoogleSocialAuthSerializer

    def post(self, request):
        """
        POST with "auth_token"
        Send an idtoken as from google to get user information
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()
        data = ((serializer.data)['auth_token'])
        return Response({"User": data}, status=status.HTTP_201_CREATED)
