from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework.authentication import BasicAuthentication
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from .user_serializer import LoginSerializer, RegistrationSerializer
from rest_framework.permissions import IsAuthenticated
from ..models import Users


class AuthUserAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        serializer = RegistrationSerializer(user)
        return Response({"user":serializer.data})



class RegisterAPIView(GenericAPIView):
    queryset = Users.objects
    serializer_class = RegistrationSerializer
    authentication_classes = []
    def post(self, request):
        serializers = self.serializer_class(data = request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(GenericAPIView):
    queryset = Users.objects
    serializer_class = LoginSerializer
    authentication_classes = []
    def post(self, request):
        password = request.data["password"]
        username = request.data["username"]

        user = authenticate(username=username, password=password)
        if user:
            serializer = self.serializer_class(user)
            return Response(serializer.data, status= status.HTTP_200_OK)
        return Response({"message":"Invalid Credentials, try again"}, status= status.HTTP_401_UNAUTHORIZED)