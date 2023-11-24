from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    email = models.EmailField(max_length=75, unique=True)
    phone = models.CharField(max_length=11, unique=True)
    counter = models.IntegerField(default=0, blank=False)
