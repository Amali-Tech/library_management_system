"""Book Request URLS file"""
from django.urls import path
from . import views


app_name = "catalogue"


urlpatterns = [
    path("book/",views.BookRequestView.as_view(),name = "book_request_list"),
    path("list/",views.ReturnBookView.as_view(),name = "book_return"),
    path("list/<int:pk>",views.ReturnBookDetailView.as_view(),name = "book_return"),
    path("booklist/",views.RequestBookListView.as_view(),name = "book_request_list"),
    path("booklist/<int:pk>/",views.RequestBookDetailView.as_view(),name = "book_list"),
]
