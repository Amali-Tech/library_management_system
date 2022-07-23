"""Authentication views for users and admin"""
import ast
import random
import string

from authentications.api.user_serializer import (
    AdminUpdateDetailSerializer, AdminUpdateSerializer,
    ChangePasswordSerializer, GoogleSocialAuthSerializer,
    LibarianRegistrationSerializer, LoginSerializer, RegistrationSerializer)
from authentications.models import GeneratedPasswords, Users
from django.contrib.auth import authenticate
from rest_framework.authentication import BasicAuthentication
from rest_framework.generics import (GenericAPIView, ListAPIView,
                                     RetrieveAPIView, UpdateAPIView)
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from google.auth.exceptions import TransportError


class IsSuperUser(IsAdminUser):
    """Checking to see if the current user is Admin user authentication"""

    def has_permission(self, request, view):
        """When called, gives the user permissions to some views"""
        return bool(request.user and request.user.is_superuser)


class AuthUserAPIView(GenericAPIView):
    """When user logs in with a token, their identity can be determines"""

    permission_classes = (IsAuthenticated,)
    serializer_class = RegistrationSerializer

    def get(self, request):
        """Getting the current logged in user info"""
        user = request.user
        serializer = AdminUpdateSerializer(user)
        return Response({
            "status":"success",
            "details": "User details found",
            "data":{
                "id":serializer.data["id"], 
                "username":serializer.data["username"],
                "email_address":serializer.data["email_address"],
                "libarian": serializer.data["is_superuser"]}})


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
            return Response({
                "status":"success",
                "details":"User created successfully",
                "data":{
                    "email_address":serializers.data["email_address"],
                    "username":serializers.data["username"]}})
        return Response({
            "status":"failure",
            "details":serializers.errors})


class LoginAPIView(GenericAPIView):
    """User and Admin login view endpoint"""
    queryset = Users.objects
    passqueryset = GeneratedPasswords.objects
    serializer_class = LoginSerializer
    authentication_classes = []


    def post(self, request):
        """Posting the details to be authenticated for access and token"""
        try:
            password = request.data["password"]
            email_address = request.data["email_address"]
            try:
                if self.passqueryset.get(password=password):
                    return Response({
                    "status":"failure",
                    "details":"Change Password"
                })
            except GeneratedPasswords.DoesNotExist:
                pass
        except KeyError:
            return Response({
                "status":"failure",
                "details":"Email and password fields required"
            })

        try:
            user = authenticate(email_address=email_address, password=password)
            if user:
                return Response({
                    "status":"success",
                    "details":"user logged in successfully",
                    "data":{
                        "email_address":user.email_address,
                        "token":user.token,
                        "libarian":user.is_superuser}})
            return Response({
                "status":"failure",
                "details":"Invalid credentials"})
        except Users.DoesNotExist:
            return Response({
                "status":"failure",
                "details":"User does not exits"
            })


class ChangePasswordAPIView(UpdateAPIView):
    """User change password view endpoint where both users can change their password"""
    model = Users
    queryset = Users.objects
    passqueryset = GeneratedPasswords.objects
    serializer_class = ChangePasswordSerializer
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        """Getting the current user object to
        update the fields in the database"""
        return self.request.user

    def update(self, request, *args, **kwargs):
        """Making a PUT request to change passowrd by both user and superuser"""
        self.object = self.get_object()
        serializer = self.serializer_class(data=request.data)
        try:
            if serializer.is_valid():
                if not self.object.check_password(serializer.data.get("old_password")):
                    return Response({
                        "status": "Wrong old password",
                        "details": "Password change unsuccessful"})
                self.object.set_password(serializer.data.get("new_password"))
                self.object.save()
                try:
                    password = self.passqueryset.get(password=serializer.data.get("old_password"))
                    if password:
                        password.delete()
                except GeneratedPasswords.DoesNotExist:
                    pass
                return Response({
                    "status":"success",
                    "details": "Password changed successfully",
                    "data": {
                        "username":self.object.username,
                        "email_address":self.object.email_address,
                        "libarian": self.object.is_superuser}})
            return Response({
                "status": "failure",
                "details": serializer.errors})
        except KeyError:
            return Response({
                "status":"failure",
                "details":"change password failed"
            })


class LibarianRegisterListView(ListAPIView, GenericAPIView):
    """Libarian registering users view endpoint"""
    characters = list(string.ascii_letters + string.digits + "!@#$%^&*()")

    def generate_random_password(self):
        """Generate random alphanumeric passwords for new user to be changed afterwards"""
        length = 25
        random.shuffle(self.characters)
        password = []
        for _ in range(length):
            password.append(random.choice(self.characters))
        random.shuffle(password)
        return "".join(password)


    queryset = Users.objects.all()
    serializer_class = AdminUpdateSerializer
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated, IsSuperUser)

    def post(self, request):
        """Post method for HTTP POST request for users to be created"""
        serializer = LibarianRegistrationSerializer(data=request.data)
        queryset = Users.objects

        if serializer.is_valid():
            password = self.generate_random_password()
            queryset.create_superuser(**serializer.data, password=password)
            password_save = GeneratedPasswords(password= password)
            password_save.save()
            return Response({
                "status": "success",
                "details":"Libarian registered successfully",
                "data": {
                    "username": serializer.data["username"],
                    "email_address": serializer.data["email_address"],
                    "password": password}})
        return Response({
            "status": "failure",
            "details": serializer.errors
            })


class LibarianDetailView(RetrieveAPIView,UpdateAPIView):
    """Superuser checking the details of other users"""
    queryset = Users.objects.all()
    serializer_class = AdminUpdateSerializer
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)

    def update(self, request, pk,*args, **kwargs):
        """Put method for superuser to control user accounts"""
        try:
            serializer = AdminUpdateDetailSerializer(data = request.data)
            if serializer.is_valid():
                queryset1 = Users.objects.filter(pk=pk)
                if queryset1:
                    queryset1.update(is_active = serializer.validated_data["is_active"])
                    queryset2 = Users.objects.get(pk=pk)
                    return Response({
                        "status":"success",
                        "details":"user status changed",
                        "data":{
                            "id":queryset2.id,
                            "username":queryset2.email_address,
                            "is_active":queryset2.is_active,
                            "libarian":queryset2.is_superuser
                            }
                    })
                else:
                    return Response({
                        "status":"failed",
                        "details":"user not found"
                    })
            else:
                return Response({
                    "status":"failure",
                    "details":serializer.errors})
        except Users.DoesNotExist:
            return Response({
                "status":"failure",
                "details":"User not found"})

    def delete(self, reqest, pk):
        """Delete User from database API"""
        try:
            queryset1 = Users.objects.get(pk=pk)
            queryset1.delete()
            return Response({
                "status": "success",
                "details": "User deleted successfully",
            })
        except Users.DoesNotExist:
            return Response({
                "status":"failure",
                "datails":"User does not exist"})


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
        try:
            serializer.is_valid()
            data = ast.literal_eval((serializer.data)['auth_token'])
            return Response({
                "status":"success",
                "detail":"User signup successful",
                "data":{
                "username": data["username"],
                "email_address":data["email"],
                "token":data["token"]}})
        except KeyError:
            return Response({
                "status":"failure",
                "details":"invalid token"
            })
        except TransportError:
            return Response({
                "status":"failure",
                "details":"Token fetch failed please check connection"
            })
        except ValueError:
            return Response({
                "status":"failure",
                "details":"Token expired"
            })
