"""Request book and approval view classes"""
from unicodedata import category

from authentications.api.views import IsSuperUser
from authentications.models import Users
from catalogue.models import Book
from reqest.api.request_serializer import (AdminReturnBookSerializer,
                                           RequestBookDetailSerializer,
                                           RequestBookListSerializer,
                                           RequestBookSerializer,
                                           ReturnBookDetailGetSerializer,
                                           ReturnBookDetailSerializer,
                                           ReturnBookGetSerializer,
                                           ReturnBookSerializer)
from reqest.models import RequestBook
from rest_framework import generics, status
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class RequestBookListView(generics.ListAPIView):
    """Admin User Request Book list API View"""
    queryset = RequestBook.objects.filter(is_requested=True, is_approved=False)
    serializer_class = RequestBookListSerializer
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated, IsSuperUser)


class RequestBookDetailView(generics.RetrieveAPIView, generics.ListAPIView):
    """Admin Request Book Detail API View to make a PUT request with ID"""
    queryset = RequestBook.objects.all()
    serializer_class = RequestBookDetailSerializer
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated, IsSuperUser)

    def put(self, request, pk):
        """Put method for HTTP PUT request from BookRequestDetailView"""
        try:
            queryset1 = RequestBook.objects.get(pk=pk)
            serializer = RequestBookDetailSerializer(queryset1, request.data)
            if serializer.is_valid():
                if serializer.validated_data["is_approved"] is True:
                    Book.objects.filter(
                        id=request.data["book"]).update(is_available=False)
                    serializer.save()
                    return Response(serializer.data)
                else:
                    Book.objects.filter(
                        id=request.data["book"]).update(is_available=True)
                    serializer.save()
                    return Response(serializer.data)
            return Response({"Unsucessful": serializer.errors})
        except RequestBook.DoesNotExist:
            return Response({
                "status":"failure",
                "details":"Request id does not exist"
            })

    def delete(self, request, pk ):
        """Delete Request from View API"""
        queryset1 = RequestBook.objects.get(pk=pk)
        queryset1.delete()
        return Response({"Sucessfully Deleted": status.HTTP_204_NO_CONTENT})


class BookRequestView(generics.CreateAPIView):
    """User Request Book view endpoint"""
    queryset = RequestBook.objects
    serializer_class = RequestBookSerializer
    authentication_classes = (BasicAuthentication,)
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """POST Request for user to request a book. If book is not available,
        A Book not available Response would be rendered."""
        serializers = self.serializer_class(data=request.data)
        try:
            if serializers.is_valid():
                book = Book.objects.get(id=request.data["book"])
                if book.is_available:
                    serializers.save(user=self.request.user)
                    return Response({
                        "status":"success",
                        "details":"book requested",
                        "data": {
                            "id":book.id,
                            "title": book.title,
                        }})
                return Response({
                "status":"failure",
                "details":"book not available"
            })
            return Response({
                    "status":"failure",
                    "details":serializers.errors
                    },status=status.HTTP_400_BAD_REQUEST)
        except Book.DoesNotExist:
            return Response({
                "status":"failure",
                "details":"enter a valid book"
            })

class ReturnBookView(generics.ListAPIView):
    """User Return Book View. This shows all books requested by user
    and approved books and not Retuned"""
    queryset = RequestBook.objects.none()
    serializer_class = ReturnBookGetSerializer
    authentication_classes = (BasicAuthentication,)
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return RequestBook.objects.filter(
            user=self.request.user
        )


class ReturnBookDetailView(generics.RetrieveAPIView, generics.UpdateAPIView):
    """Returning of books requested by user and updating the book to
    make it available for users"""
    queryset = RequestBook.objects.all()
    serializer_class = ReturnBookDetailGetSerializer
    authentication_classes = (BasicAuthentication,)

    def put(self, request, pk):
        """Put method for HTTP PUT request from RetunrBookDetailView for user to update that
        they want to return a book."""
        try:
            queryset1 = RequestBook.objects.get(pk=pk)
            serializer = ReturnBookDetailSerializer(queryset1, data=request.data)
            if serializer.is_valid():
                book = Book.objects.get(id=queryset1.book_id)
                serializer.save()
                return Response({
                    "status":"success",
                    "details":"book returned, waiting approval",
                    "data":{
                        "book":book.title,
                        "is_returned":serializer.data["is_returned"]
                    }
                })
            return Response({"Unsucessful": serializer.errors})
        except RequestBook.DoesNotExist:
            return Response({
                "status":"failure",
                "details":"request does not exist"
            })

class AdminViewReturnBookView(generics.ListAPIView):
    """Admin User Return Book View. This shows all books requested by user
    and approved books and not Retuned"""
    queryset = RequestBook.objects.none()
    serializer_class = AdminReturnBookSerializer
    authentication_classes = (BasicAuthentication,)
    permission_classes = [IsAuthenticated,IsSuperUser]

    def get_queryset(self):
        request_try = RequestBook.objects
        requests = request_try.filter(is_approved = True,is_returned=False)
        request_book_id = requests.values_list("user_id", flat=True)
        users = Users.objects.filter(id__in=request_book_id)
        for user in users:
            current = request_try.filter(user_id=user.id)
            for i in current:
                if i.expiry is None:
                    i.expiry = datetime.min
                elif i.updated >= i.expiry:
                    user.update(is_active =False)
        return requests

class AdminViewReturnedBooksToApproveView(generics.ListAPIView,generics.UpdateAPIView):
    """Admin User Return Book View. This shows all books requested by user
    and approved books and not Retuned"""
    queryset = RequestBook.objects.filter(is_approved = True,is_returned=True)
    serializer_class = AdminReturnBookSerializer
    authentication_classes = (BasicAuthentication,)
    permission_classes = [IsAuthenticated,IsSuperUser]
    
class AdminViewReturnedBooksToApproveDetailView(generics.ListAPIView,generics.UpdateAPIView):
    """Admin User Return Book View. This shows all books requested by user
    and approved books and not Retuned"""
    queryset = RequestBook.objects.filter(is_approved = True,is_returned=True)
    serializer_class = AdminReturnBookSerializer
    authentication_classes = (BasicAuthentication,)
    permission_classes = [IsAuthenticated,IsSuperUser]
    
    def put(self, request, pk):
        """Put method for HTTP PUT request from RetunrBookDetailView for user to update that
        they want to return a book."""
        queryset1 = RequestBook.objects.get(pk=pk)
        serializer = AdminReturnBookSerializer(queryset1, request.data)
        if serializer.is_valid():
            Book.objects.filter(id=request.data["book"]).update(is_available=True)
            serializer.save()
            return Response(serializer.data)
        return Response({"Unsucessful": serializer.errors})
