"""Creation of models for Book catalogue"""

from django.db import models
from django.utils.text import slugify
# Create your models here.


class Category(models.Model):
    """Books category of the catalogue"""
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        """Ordering by name"""
        ordering = ("name",)
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self):
        """Returning the readable name of model"""
        return f"{self.name}"

    def save(self, *args, **kwargs):
        """Overiding the save method of Model
        to slugify the name input by user"""
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)


class Book(models.Model):
    """Definition of book model"""
    category = models.ForeignKey(
        Category, related_name="books", on_delete=models.CASCADE)
    title = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    description = models.TextField()
    is_available = models.BooleanField(default=False)
    image = models.ImageField(upload_to='images/%Y/%m/%d',blank=True)

    class Meta:
        """Ordering by title"""
        ordering = ("title",)
        verbose_name = "book"
        verbose_name_plural = "books"

    def __str__(self):
        """Returning the human readable name of the class"""
        return f"{self.title}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
