"""Views for the serialized data from database"""
from authentications.api.views import IsSuperUser
from catalogue.api.catalog_serializer import (BookSerializer,
                                              BookSerializerAdmin,
                                              CategorySerializer)
from rest_framework import generics, status
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from catalogue.models import Book, Category


class BookListView(generics.ListAPIView):
    """Book list API View"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)


class AdminBookListView(generics.ListAPIView):
    """Book list API View"""
    queryset = Book.objects.all()
    serializer_class = BookSerializerAdmin
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated, IsSuperUser)

    def post(self, request, *args, **kwargs):
        """Post method for HTTP POST request from Booklist View"""
        serializer = BookSerializerAdmin(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "details": "book added successfully",
                "data": {
                    "category_id": serializer.data["category"],
                    "title": serializer.data["title"],
                    "description": serializer.data["description"],
                    "is_available": serializer.data["is_available"],
                    "image": serializer.data["image"]
                }
            })
        return Response({
            "status": "failure",
            "details": serializer.errors})


class BookDetailView(generics.RetrieveAPIView):
    """Book Detail API View to make a PUT request with ID"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,IsSuperUser)

    def put(self, request, pk):
        """Put method for HTTP PUT request from BookDetailView"""
        try:
            queryset1 = Book.objects.get(pk=pk)
            serializer = BookSerializerAdmin(queryset1, request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "status": "success",
                    "details": "Book updated successfully",
                    "data": {
                        "category_id": serializer.data["category"],
                        "title": serializer.data["title"],
                        "description": serializer.data["description"],
                        "is_available": serializer.data["is_available"],
                        "image": serializer.data["image"]
                    }
                })
            else:
                return Response({
                    "status": "failure",
                    "details": serializer.errors
                })
        except Book.DoesNotExist:
            return Response({
                "status": "failure",
                "details": "book does not exist"
            })

    def delete(self, request, pk):
        """Delete Book from catalog View API"""
        try:
            queryset1 = Book.objects.get(pk=pk)
            queryset1.delete()
            return Response({
                "status": "success",
                "details":"book deleted"
            })
        except Book.DoesNotExist:
            return Response({
                "status": "failure",
                "details": "book does not exist"
            })


class CategoryView(generics.ListAPIView):
    """Catalogue list API View"""
    queryset = Category.objects
    serializer_class = CategorySerializer
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated, IsSuperUser)

    def post(self, request):
        """Post method for HTTP POST request from Catalogue View"""
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "details": "catalogue created",
                "data": {
                    "id": serializer.data["id"],
                    "name": serializer.data["name"]
                }})
        return Response({
            "status": "failure",
            "details": serializer.errors})


class CategoryDetailView(generics.RetrieveAPIView):
    """Category Detail API View to make a PUT request with ID"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated, IsSuperUser)

    def put(self, request, pk):
        """Put method for HTTP PUT request from CategoryDetailView"""
        try:
            queryset1 = Category.objects.get(pk=pk)
            serializer = CategorySerializer(queryset1, request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "status": "success",
                    "details": "category updated",
                    "data": {
                        "id": serializer.data["id"],
                        "name": serializer.data["name"]
                    }
                })
            else:
                return Response({
                    "status": "failure",
                    "details": serializer.errors
                })

        except Category.DoesNotExist:
            return Response({
                "status": "failure",
                "details": "category does not exist"
            })

    def delete(self, request, pk):
        """Delete Catalogue from catalog View API with ID"""
        try:
            querry = Category.objects.get(pk=pk)
            querry.delete()
            return Response({
                "status": "success",
                "details":"category deleted"})
        except Category.DoesNotExist:
            return Response({
                "status": "failure",
                "details": "category does not exit"
            })
