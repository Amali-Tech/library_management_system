"""library URL Configuration"""
from django.contrib import admin
from django.urls import path, include
from authentications.api.user_serializer import GoogleLogin


urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include("catalogue.api.urls", namespace="api")),
    path("user/", include("authentications.api.urls",namespace="users")),
    path('user/password_reset/', include('django_rest_passwordreset.urls',
    namespace='password_reset')),
    path('social-login/google/', GoogleLogin.as_view(), name='google_login'),
    path("users/request/", include("reqest.api.urls", namespace="request"))
]
