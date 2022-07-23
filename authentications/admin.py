"""Admin User file"""
from django.contrib import admin
from .models import Users,GeneratedPasswords
# Register your models here.

@admin.register(Users)
class UserAdmin(admin.ModelAdmin):
    """Registration of User model class in admin"""
    list_display = ("username","email_address","is_active","is_superuser")
    list_display_links =("username",)
    list_editable = ("email_address",)

@admin.register(GeneratedPasswords)
class Passwords(admin.ModelAdmin):
    """Generated passwords save"""
    list_display = ("password",)
