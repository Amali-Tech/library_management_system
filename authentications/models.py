"""Models for user creation"""
from datetime import datetime, timedelta

from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.conf import settings

import jwt


# Create your models here.
class Libarian(BaseUserManager):
    """Registration of the user using the BaseUserManager to create a superuser"""

    def create_user(self, email_address, username=None, password=None):
        """Creation of user"""
        if not email_address:
            raise ValueError("user must have email address")

        user = self.model(
            email_address=email_address,
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email_address, password, username=None):
        """Creation of a superuser"""
        user = self.create_user(
            username=username, email_address=email_address, password=password)
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Users(AbstractBaseUser):
    """User creation model"""
    email_address = models.EmailField(
        verbose_name='email', unique=True, max_length=200)
    username = models.CharField(max_length=200, blank=False, unique=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email_address'
    REQUIRED_FIELDS = ["username"]
    objects = Libarian()

    class Meta:
        """Pre displayed field"""
        ordering = ("email_address",)

    def __str__(self):
        return f"{self.email_address}"

    def has_perm(self, perm, obj=None):
        """When user registraion has permission, then it is a superuser"""
        return self.is_superuser

    def has_module_perms(self, app_label):
        """Has permission to access the model, like create a super user"""
        return self.is_superuser

    @property
    def token(self):
        """Token generator for user to use to login"""
        token = jwt.encode({"username": self.username, "email": self.email_address,
                            "exp": datetime.utcnow() + timedelta(hours=24)},
                           settings.SECRET_KEY, algorithm="HS256")
        return token

class GeneratedPasswords(models.Model):
    """Table for generated passwords for libarians"""
    password = models.CharField(unique=False, blank=False,max_length=25)

    class Meta:
        """Pre defined fields"""
        ordering = ("password",)

    def __str__(self):
        """Returning the human readable name of the class"""
        return f"{self.password}"
