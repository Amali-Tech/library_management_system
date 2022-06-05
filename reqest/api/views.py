"""Request book and approval view classes"""
from datetime import datetime

from authentications.api.views import IsSuperUser
from authentications.models import Users
from catalogue.models import Book
from reqest.api.request_serializer import (AdminApprovedButNotReturnedBook,
                                           AdminRequestBookDetailSerializer,
                                           AdminReturnBookSerializer,
                                           RequestBookDetailSerializer,
                                           RequestBookListSerializer,
                                           RequestBookSerializer,
                                           ReturnBookDetailGetSerializer,
                                           ReturnBookDetailSerializer,
                                           ReturnBookGetSerializer)
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
            serializer = AdminRequestBookDetailSerializer(queryset1, data =request.data)
            if serializer.is_valid():
                book_name = Book.objects.get(id=queryset1.book_id)
                book  =Book.objects.filter(id=queryset1.book_id)
                if serializer.validated_data["is_approved"] is True:
                    book.update(is_available=False)
                    serializer.save()
                    return Response({
                        "status":"success",
                        "details":"request approved",
                        "data":{
                            "id":queryset1.id,
                            "book":book_name.title,
                            "is_approved":queryset1.is_approved
                        }
                        })
                else:
                    Book.objects.filter(
                        id=queryset1.book_id).update(is_available=True)
                    serializer.save()
                    return Response({
                        "status":"success",
                        "details":"request unapproved",
                        "data":{
                            "id":queryset1.id,
                            "book":book_name.title,
                            "is_approved":queryset1.is_approved
                        }
                        })
            return Response({"Unsucessful": serializer.errors})
        except RequestBook.DoesNotExist:
            return Response({
                "status":"failure",
                "details":"Request id does not exist"
            })
        except KeyError:
            return Response({
                "status":"failure",
                "details":"is_approved required"
            })

    def delete(self, request, pk ):
        """Delete Request from View API"""
        try:
            queryset1 = RequestBook.objects.get(pk=pk)
            queryset1.delete()
            return Response({
                "status":"success",
                "details":"request deleted"
            })
        except RequestBook.DoesNotExist:
            return Response({
                "status":"failure",
                "details":"Request does not exist",
            })


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
                if queryset1.is_approved:
                    if serializer.validated_data["is_returned"] is True:
                        serializer.save()
                        return Response({
                            "status":"success",
                            "details":"book returned, waiting approval",
                            "data":{
                                "book":book.title,
                                "is_returned":serializer.data["is_returned"]
                            }
                        })
                    elif queryset1.is_approved_return:
                        return Response({
                            "status":"failure",
                            "details":"book return already approved"
                    })
                    else:
                        serializer.save()
                        return Response({
                            "status":"success",
                            "details":"return retracted",
                            "data":{
                                "book":book.title,
                                "is_returned":serializer.data["is_returned"]
                            }
                        })

                return Response({
                    "status":"failure",
                    "details":"book not approved yet"
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
    serializer_class = AdminApprovedButNotReturnedBook
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
    serializer_class = AdminApprovedButNotReturnedBook
    authentication_classes = (BasicAuthentication,)
    permission_classes = [IsAuthenticated,IsSuperUser]

class AdminViewReturnedBooksToApproveDetailView(generics.ListAPIView,generics.UpdateAPIView):
    """Admin User Return Book View. This shows all books requested by user
    and approved books and not Retuned"""
    queryset = RequestBook.objects.filter(is_approved = True,is_returned=True)
    serializer_class = AdminApprovedButNotReturnedBook
    authentication_classes = (BasicAuthentication,)
    permission_classes = [IsAuthenticated,IsSuperUser]

    def put(self, request, pk):
        """Put method for HTTP PUT request from RetunrBookDetailView for user to update that
        they want to return a book."""
        try:
            queryset1 = RequestBook.objects.get(pk=pk)
            serializer = AdminReturnBookSerializer(queryset1, request.data)
            if serializer.is_valid():
                if serializer.validated_data["is_approved_return"]:
                    Book.objects.filter(id=queryset1.book_id).update(is_available=True)
                    serializer.save()
                    return Response({
                        "status":"success",
                        "details":"book return approved",
                        "data":{
                            "id":queryset1.id,
                            "is_approved": queryset1.is_approved,
                            "is_returned":queryset1.is_returned,
                            "is_approved_return":queryset1.is_approved_return,
                        }
                    })
                else:
                    Book.objects.filter(id=queryset1.book_id).update(is_available=False)
                    serializer.save()
                    return Response({
                        "status":"success",
                        "details":"book return disapproved",
                        "data":{
                            "id":queryset1.id,
                            "is_approved": queryset1.is_approved,
                            "is_returned":queryset1.is_returned,
                            "is_approved_return":queryset1.is_approved_return,
                        }
                    })
            return Response({
                "status":"failure",
                "details":serializer.errors
            })
        except RequestBook.DoesNotExist:
            return Response({
                "status":"failure",
                "details":"request does not exist"
            })
