"""Admin User file"""
from django.contrib import admin
from .models import Users
# Register your models here.

@admin.register(Users)
class UserAdmin(admin.ModelAdmin):
    """Registration of User model class in admin"""
    list_display = ("username","Email_Address","is_active",)
