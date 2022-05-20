from rest_framework import generics
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from .api.user_serializer import RegistrationSerializer
from .models import Users
# Create your views here.

class LibarianRegisterListView(generics.ListAPIView):
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
    

class LibarianDetailView(generics.RetrieveAPIView):
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

    def delete(self, pk):
        """Delete Book from catalog View API"""
        queryset1 = Users.objects.get(pk=pk)
        queryset1.delete()
        return Response({"Sucessfully Deleted":'okay'})
