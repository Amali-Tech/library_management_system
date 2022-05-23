"""Model for RequestBook"""
from django.db import models
from authentications.models import Users
from catalogue.models import Book



# Create your models here.
class RequestBook(models.Model):
    """Model for Request Book"""
    user = models.ForeignKey(Users,on_delete=models.CASCADE, related_name="request_book")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="books_to_request")
    request = models.BooleanField(default=True)
    approval = models.BooleanField(default=False)
    returned = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        """Pre ordered and displayed by Approval"""
        ordering = ("approval",)
    def __str__(self):
        return f"{self.user},{self.book}"
