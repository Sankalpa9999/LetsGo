from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True, null=False)
    username = models.CharField(max_length=50, unique=True)

    REQUIRED_FIELDS = ['username']
    USERNAME_FIELD = 'email'

    Bio = models.TextField(max_length=500, blank=True, null=True)

    # Only in User model
    profile_image = models.ImageField(upload_to='user_profile_images/', default='default.jpg', blank=True, null=True)
    document_image = models.ImageField(upload_to='user_documents/', blank=True, null=True)

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    verified = models.BooleanField(default=False)

    @property
    def image(self):
        # Always return the user's profile image
        return self.user.profile_image

    @property
    def document(self):
        # Access the document image from the user
        return self.user.document_image

    def __str__(self):
        return self.full_name or self.user.username
    
    
    
class ContactUs(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    subject = models.CharField(max_length=100, blank=True, null=True)
    message = models.TextField(max_length=500, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    
    class Meta:
        verbose_name = 'ContactUs'
        verbose_name_plural = 'ContactUs'
    
    
    def __str__(self):
        return self.name