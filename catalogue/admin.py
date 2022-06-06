"""Admin class for testing models"""
from django.contrib import admin
from catalogue.models import Category, Book
# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Registering the category model as Admin model"""
    list_display = ("name", "slug",)
    list_filter = ["name"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """Registering Book model class as Admin model"""
    list_display = ("category", "title", "is_available",)
    list_filter = ["title"]
    prepopulated_fields = {"slug": ("title",)}
