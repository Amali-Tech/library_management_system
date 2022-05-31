"""Models for user creation"""
from datetime import datetime, timedelta

from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.conf import settings

import jwt


# Create your models here.
class Libarian(BaseUserManager):
    """Registration of the user using the BaseUserManager to create a superuser"""

    def create_user(self, Email_Address, username, password=None):
        """Creation of user"""
        if not Email_Address:
            raise ValueError("user must have email address")

        user = self.model(
            Email_Address=Email_Address,
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, Email_Address, password):
        """Creation of a superuser"""
        user = self.create_user(
            username=username, Email_Address=Email_Address, password=password)
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Users(AbstractBaseUser):
    """User creation model"""
    Email_Address = models.EmailField(
        verbose_name='email', unique=False, blank=True, max_length=200, default=None)
    username = models.CharField(max_length=200, blank=True, unique=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ["Email_Address"]
    objects = Libarian()

    class Meta:
        """Pre displayed field"""
        ordering = ("username",)

    def __str__(self):
        return f"{self.Email_Address}, {self.username}"

    def has_perm(self, perm, obj=None):
        """When user registraion has permission, then it is a superuser"""
        return self.is_superuser

    def has_module_perms(self, app_label):
        """Has permission to access the model, like create a super user"""
        return self.is_superuser

    @property
    def token(self):
        """Token generator for user to use to login"""
        token = jwt.encode({"username": self.username, "email": self.Email_Address,
                            "exp": datetime.utcnow() + timedelta(hours=24)},
                           settings.SECRET_KEY, algorithm="HS256")
        return token
