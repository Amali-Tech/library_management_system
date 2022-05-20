from django.urls import path
from . import views


app_name = "users"
urlpatterns = [
    path("list/", views.LibarianRegisterListView.as_view(), name = "user_list"),
    path("list/<pk>",views.LibarianDetailView.as_view(),name = "user_detail")
]
