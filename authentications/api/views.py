from django.contrib.auth import authenticate
from rest_framework.authentication import BasicAuthentication
from rest_framework.generics import GenericAPIView,UpdateAPIView,ListAPIView,RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..models import Users
from .user_serializer import LoginSerializer, RegistrationSerializer, ChangePasswordSerializer


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

class ChangePasswordAPIView(UpdateAPIView):
    model = Users
    queryset = Users.objects
    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self,queryset=None):
        return self.request.user
    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            print(serializer.data)
            if not self.object.check_password(serializer.data.get("old_password")):
                print(serializer.data.get("old_password"))
                return Response({"old_password": ["Wrong password."]},
                status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response({"Status":"Success","Message":"Password changed successfully"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LibarianRegisterListView(ListAPIView):
    queryset = Users.objects
    serializer_class = RegistrationSerializer
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        """Post method for HTTP POST request from Users View"""
        serializer = RegistrationSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Added Libarian":request.data})
        return Response({"Was not able to add Libarian":request.data})
    

class LibarianDetailView(RetrieveAPIView):
    queryset = Users.objects.all()
    serializer_class = RegistrationSerializer
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)
    def put(self,request,pk):
        """Put method for HTTP PUT request from BookDetailView"""
        queryset1 = Users.objects.get(pk=pk)
        serializer = RegistrationSerializer(queryset1, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

    def delete(self,reqest,pk):
        """Delete Book from catalog View API"""
        queryset1 = Users.objects.get(pk=pk)
        queryset1.delete()
        return Response({"Sucessfully Deleted":'okay'})
