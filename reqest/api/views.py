"""Request book and approval view classes"""
from datetime import datetime, timedelta
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from authentications.api.views import IsSuperUser
from reqest.models import RequestBook
from catalogue.models import Book
from authentications.models import Users
from reqest.api.request_serializer import RequestBookSerializer, RequestBookListSerializer, RequestBookDetailSerializer, ReturnBookSerializer, ReturnBookDetailSerializer,AdminReturnBookSerializer


class RequestBookListView(generics.ListAPIView):
    """Admin User Request Book list API View"""
    queryset = RequestBook.objects.filter(request=True, approval=False)
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
        queryset1 = RequestBook.objects.get(pk=pk)
        serializer = RequestBookDetailSerializer(queryset1, request.data)
        if serializer.is_valid():
            if serializer.validated_data["approval"] is True:
                Book.objects.filter(
                    id=request.data["book"]).update(available=False)
                serializer.save()
                return Response(serializer.data)
            else:
                Book.objects.filter(
                    id=request.data["book"]).update(available=True)
                serializer.save()
                return Response(serializer.data)
        return Response({"Unsucessful": serializer.errors})

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
        if Book.objects.get(id=request.data["book"]).available:
            if serializers.is_valid():
                serializers.save(user=self.request.user)
                return Response({"Book Requested Successfully": serializers.data},
                status=status.HTTP_201_CREATED)
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response("Book not available", status=status.HTTP_401_UNAUTHORIZED)


class ReturnBookView(generics.ListAPIView):
    """User Return Book View. This shows all books requested by user
    and approved books and not Retuned"""
    queryset = RequestBook.objects.none()
    serializer_class = ReturnBookSerializer
    authentication_classes = (BasicAuthentication,)
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return RequestBook.objects.filter(
            user=self.request.user, returned=False
        )


class ReturnBookDetailView(generics.RetrieveAPIView, generics.UpdateAPIView):
    """Returning of books requested by user and updating the book to
    make it available for users"""
    queryset = RequestBook.objects.all()
    serializer_class = ReturnBookDetailSerializer
    authentication_classes = (BasicAuthentication,)

    def put(self, request, pk):
        """Put method for HTTP PUT request from RetunrBookDetailView for user to update that
        they want to return a book."""
        queryset1 = RequestBook.objects.get(pk=pk)
        serializer = ReturnBookDetailSerializer(queryset1, request.data)
        if serializer.is_valid():
            Book.objects.filter(id=request.data["book"]).update(available=True)
            serializer.save()
            return Response(serializer.data)
        return Response({"Unsucessful": serializer.errors})

class AdminViewReturnBookView(generics.ListAPIView):
    """Admin User Return Book View. This shows all books requested by user
    and approved books and not Retuned"""
    queryset = RequestBook.objects.none()
    serializer_class = AdminReturnBookSerializer
    authentication_classes = (BasicAuthentication,)
    permission_classes = [IsAuthenticated,IsSuperUser]

    def get_queryset(self):
        request_try = RequestBook.objects
        requests = request_try.filter(approval = True,returned=False)
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
    queryset = RequestBook.objects.filter(approval = True,returned=True)
    serializer_class = AdminReturnBookSerializer
    authentication_classes = (BasicAuthentication,)
    permission_classes = [IsAuthenticated,IsSuperUser]
    
class AdminViewReturnedBooksToApproveDetailView(generics.ListAPIView,generics.UpdateAPIView):
    """Admin User Return Book View. This shows all books requested by user
    and approved books and not Retuned"""
    queryset = RequestBook.objects.filter(approval = True,returned=True)
    serializer_class = AdminReturnBookSerializer
    authentication_classes = (BasicAuthentication,)
    permission_classes = [IsAuthenticated,IsSuperUser]
    
    def put(self, request, pk):
        """Put method for HTTP PUT request from RetunrBookDetailView for user to update that
        they want to return a book."""
        queryset1 = RequestBook.objects.get(pk=pk)
        serializer = AdminReturnBookSerializer(queryset1, request.data)
        if serializer.is_valid():
            print(serializer.validated_data["approval"])
            Book.objects.filter(id=request.data["book"]).update(available=True)
            serializer.save()
            return Response(serializer.data)
        return Response({"Unsucessful": serializer.errors})
    