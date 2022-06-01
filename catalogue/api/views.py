"""Views for the serialized data from database"""
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from ..models import Book, Category
from .catalog_serializer import BookSerializer,CategorySerializer


class BookListView(generics.ListAPIView):
    """Book list API View"""
    queryset = Book.objects.filter(available=True)
    serializer_class = BookSerializer
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        """Post method for HTTP POST request from Booklist View"""
        serializer = BookSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Added Book":request.data})
        return Response({"Was not able to add category":request.data})


class BookDetailView(generics.RetrieveAPIView):
    """Book Detail API View to make a PUT request with ID"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)

    def put(self,request,pk):
        """Put method for HTTP PUT request from BookDetailView"""
        queryset1 = Book.objects.get(pk=pk)
        serializer = BookSerializer(queryset1, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

    def delete(self, request, pk):
        """Delete Book from catalog View API"""
        queryset1 = Book.objects.get(pk=pk)
        queryset1.delete()
        return Response({"Sucessfully Deleted":status.HTTP_204_NO_CONTENT})

class CategoryView(generics.ListAPIView):
    """Catalogue list API View"""
    queryset = Category.objects
    serializer_class = CategorySerializer
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        """Post method for HTTP POST request from Catalogue View"""
        serializer = CategorySerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Added category":request.data})
        return Response({"Was not able to add category":request.data})


class CategoryDetailView(generics.RetrieveAPIView):
    """Category Detail API View to make a PUT request with ID"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)

    def put(self,request,pk):
        """Put method for HTTP PUT request from CategoryDetailView"""
        queryset1 = Category.objects.get(pk=pk)
        serializer = CategorySerializer(queryset1, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

    def delete(self,request,pk):
        """Delete Catalogue from catalog View API with ID"""
        querry = Category.objects.get(pk=pk)
        querry.delete()
        return Response({"Successfully Deleted": status.HTTP_204_NO_CONTENT})
