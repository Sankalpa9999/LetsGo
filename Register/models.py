from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    # You can add other fields if needed
    # Example:
    # phone_number = models.CharField(max_length=15, blank=True)
    # address = models.TextField(blank=True)

    def __str__(self):
        return self.user.email