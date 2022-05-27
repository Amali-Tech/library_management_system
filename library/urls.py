"""library URL Configuration"""
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include("catalogue.api.urls", namespace="api")),
    path("user/", include("authentications.api.urls",namespace="users")),
    path('user/password_reset/', include('django_rest_passwordreset.urls',
    namespace='password_reset')),
    path("users/request/", include("reqest.api.urls", namespace="request")),
]
