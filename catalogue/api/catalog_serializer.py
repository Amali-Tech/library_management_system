"""Catalogue serializer class"""
from rest_framework import serializers
from catalogue.models import Book, Category


class BookSerializer(serializers.ModelSerializer):
    """Book serializer class"""
    category = serializers.ReadOnlyField(source ="category.name")
    class Meta:
        """Modeling from the Book model class"""
        model = Book
        fields = ["id", "category", "title",
                  "description", "is_available", "image"]

class BookSerializerAdmin(serializers.ModelSerializer):
    """Book serializer class"""
    class Meta:
        """Modeling from the Book model class"""
        model = Book
        fields = ["id", "category", "title",
                  "description", "is_available", "image"]


class CategorySerializer(serializers.ModelSerializer):
    """Category serializer class"""
    class Meta:
        """Serializing from Category Model class"""
        model = Category
        fields = ["id", "name"]
