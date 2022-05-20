from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.conf import settings
import jwt
# Create your models here.
from datetime import datetime, timedelta

class Libarian(BaseUserManager):
    """Registration of the user"""

    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("user must have email address")

        user = self.model(
            Email_Address=email,
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, Email_Address, password):
        user = self.create_user(username=username, email=
            Email_Address, password=password)
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)


class Users(AbstractBaseUser):
    Email_Address = models.EmailField(
        verbose_name='email', unique=False, blank=True, max_length=200, default=None)
    username = models.CharField(max_length=200, blank=True, unique=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ["Email_Address"]
    objects = Libarian()

    class Meta:
        ordering = ("username",)

    def __str__(self):
        return f"{self.Email_Address}"

    def has_perm(self, perm, obj=None): 
        return self.is_superuser

    def has_module_perms(self, app_label): 
        return self.is_superuser

    @property
    def token(self):
        token= jwt.encode({"username":self.username,"email":self.Email_Address,
        "exp":datetime.utcnow() + timedelta(hours=24)},
        settings.SECRET_KEY, algorithm="HS256")
        return token
