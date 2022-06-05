"""Book request and approval Serializer class"""
from rest_framework import serializers
from reqest.models import RequestBook


class RequestBookSerializer(serializers.ModelSerializer):
    """User Request Book serializer class"""

    class Meta:
        """Modeling from the Book model class"""
        model = RequestBook
        fields = ["id", "book"]


class RequestBookDetailSerializer(serializers.ModelSerializer):
    """Request Book details"""
    book = serializers.CharField(max_length=200)
    """Admin Book Request Detail View serializer class"""
    class Meta:
        """Modeling from the RequestBook model class"""
        model = RequestBook
        fields = ["id", "book", "is_approved"]

class AdminRequestBookDetailSerializer(serializers.ModelSerializer):
    """Admin Book Request Detail View serializer class"""
    class Meta:
        """Modeling from the RequestBook model class"""
        model = RequestBook
        fields = ["is_approved"]


class RequestBookListSerializer(serializers.ModelSerializer):
    """Admin all user Book Request List serializer class"""
    user = serializers.CharField(max_length=200)
    book = serializers.CharField(max_length=200)

    class Meta:
        """Modeling from the Request Book model class"""
        model = RequestBook
        fields = ["id", "user", "book",
                  "is_requested", "is_approved", "is_returned"]

class ReturnBookGetSerializer(serializers.ModelSerializer):
    """User return book serializer class"""
    book = serializers.ReadOnlyField(source = "book.title")
    class Meta:
        """Pre displayed for user to see and update"""
        model = RequestBook
        fields = ["id", "book", "is_approved", "is_returned"]


class AdminReturnBookSerializer(serializers.ModelSerializer):
    """Admin checking returned books to approve serializer class"""
    class Meta:
        """Pre displayed for user to see and update"""
        model = RequestBook
        fields = ["is_approved_return"]

class AdminApprovedButNotReturnedBook(serializers.ModelSerializer):
    """Admin checking returned books to approve serializer class"""
    book = serializers.CharField(max_length = 200)
    user = serializers.CharField(max_length =200)
    class Meta:
        """Pre displayed for user to see and update"""
        model = RequestBook
        fields = ["id", "user", "book", "is_approved", "is_returned", "is_approved_return"]


class ReturnBookDetailSerializer(serializers.ModelSerializer):
    """User Return Book view"""
    class Meta:
        """required fields"""
        model = RequestBook
        fields = ["is_returned"]


class ReturnBookDetailGetSerializer(serializers.ModelSerializer):
    """User Return Book view"""
    book = serializers.ReadOnlyField(source = "book.title")
    class Meta:
        """required fields"""
        model = RequestBook
        fields = ["id", "book", "is_returned"]
