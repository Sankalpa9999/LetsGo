from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    email = models.EmailField(unique=True, null=False)
    username = models.CharField(max_length=50, unique=True)
    
    REQUIRED_FIELDS = ['username']
    USERNAME_FIELD = 'email'
    Bio = models.TextField(max_length=500)
    
    
    def __str__(self):
        return self.username