"""JWT Token Authentication for user login"""
from httplib2 import Response
import jwt
from rest_framework import exceptions
from rest_framework.authentication import get_authorization_header, BaseAuthentication
from django.conf import settings
from authentications.models import Users


class JWTBaseAuthentication(BaseAuthentication):
    """JWT Token generating from user register class"""
    def authenticate(self, request):
        """Authentication Method"""
        auth_hearder = get_authorization_header(request)
        auth_data = auth_hearder.decode('utf-8')
        auth_token = auth_data.split(" ")
        if len(auth_token) != 2:
            raise exceptions.AuthenticationFailed("Token not valid")
        token = auth_token[1]
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms="HS256")
            username = payload["username"]
            user = Users.objects.get(username=username)
            return (user, token)

        except jwt.ExpiredSignatureError as exc:
            raise exceptions.AuthenticationFailed("Token Expired, login again") from exc

        except jwt.DecodeError as exc:
            raise exceptions.AuthenticationFailed("Token is invalid") from exc

        except Users.DoesNotExist as exc:
            raise exceptions.AuthenticationFailed("No such user") from exc
        except ValueError:
            return Response({
                "status":"failure",
                "details":"Token expired"
            })
