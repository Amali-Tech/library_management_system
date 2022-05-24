"""Model for RequestBook"""
from datetime import datetime, timedelta
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
    expiry = models.DateTimeField(null=True)
    class Meta:
        """Pre ordered and displayed by Approval"""
        ordering = ("approval",)
    def __str__(self):
        return f"{self.user},{self.book}"

    def save(self, *args, **kwargs):
        """Overiding the save method of Model
        to save the 1 month expiry date after approval by user"""
        if self.approval is False:
            self.expiry = datetime.max
            super(RequestBook, self).save(*args, **kwargs)
        else:
            current_time = datetime.now()
            one_month_date = current_time + timedelta(days = 31)
            self.expiry = one_month_date
            super(RequestBook, self).save(*args, **kwargs)
