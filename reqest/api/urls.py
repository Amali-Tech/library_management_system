"""Book Request URLS file"""
from django.urls import path
from reqest.api import views


app_name = "catalogue"


urlpatterns = [
    path("book/",views.BookRequestView.as_view(),name = "book_request_list"),
    path("admin/list/",views.AdminViewReturnBookView.as_view(),name = "Admin_book_request_list"),
    path("list/",views.ReturnBookView.as_view(),name = "book_return"),
    path("list/<int:pk>/",views.ReturnBookDetailView.as_view(),name = "book_return"),
    path("admin/return/<int:pk>/",views.AdminViewReturnedBooksToApproveDetailView.as_view(),
    name = "book_return_approve"),
    path("admin/return/",views.AdminViewReturnedBooksToApproveView.as_view(),
    name = "book_return_approved"),
    path("booklist/",views.RequestBookListView.as_view(),name = "book_request_list"),
    path("booklist/<int:pk>/",views.RequestBookDetailView.as_view(),name = "book_list"),
]
