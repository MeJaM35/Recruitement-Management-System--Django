from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    username = models.CharField(max_length=20, unique=True, null=True)
    email = models.EmailField(unique=True, null=True)
    fname = models.CharField(max_length=20, null=True)
    lname = models.CharField(max_length=20, null=True)
    bio = models.TextField(blank=True, null=True)
    pronouns = models.CharField(max_length=10, null=True, blank=True)
    pfp = models.ImageField(upload_to='pfps', null=True, blank=True, default='default.jpg')
    is_writer = models.BooleanField(null=True, default=False)

    def __str__(self):
        return self.username

    REQUIRED_FIELDS = ['email']

# Create your models here.
