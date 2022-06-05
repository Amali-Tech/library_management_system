"""Admin for Request applications"""
from django.contrib import admin
from reqest.models import RequestBook

# Register your models here.
@admin.register(RequestBook)


class RequestAdmin(admin.ModelAdmin):
    """Registration of Request Book in Admin"""
    list_display = ["user","book","is_requested","is_approved"]
