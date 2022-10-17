from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

# Create your models here. 

class User(AbstractUser):
    name = models.CharField(max_length=255, blank=True)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # token = models.CharField('tele-token', max_length=255, blank=True)