"""Authentications URLS File"""
from django.urls import path
from . import views


app_name = "userss"


urlpatterns = [
    path("register/", views.RegisterAPIView.as_view(), name="register"),
    path("login/", views.LoginAPIView.as_view(), name="login"),
    path("detail/", views.AuthUserAPIView.as_view(), name="user"),
    path("passwordchange/", views.ChangePasswordAPIView.as_view(), name="user"),
    path("list/", views.LibarianRegisterListView.as_view(), name="user_list"),
    path("list/<pk>/", views.LibarianDetailView.as_view(), name="user_detail")

]
