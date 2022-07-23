"""library URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from catalogue.api import views

app_name = "catalogue"
urlpatterns = [
    path("books/",views.BookListView.as_view(),name = "book_list"),
    path("admin/books/",views.AdminBookListView.as_view(),name = "admin_book_list"),
    path("books/<pk>/", views.BookDetailView.as_view(), name= "book_detail"),
    path("catalog/", views.CategoryView.as_view(), name = "category_list"),
    path("catalog/<pk>", views.CategoryDetailView.as_view(), name = "category_list"),
]
