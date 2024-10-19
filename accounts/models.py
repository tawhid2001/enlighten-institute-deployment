from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('teacher','Teacher'),
        ('student','Student'),
    )

    user_type = models.CharField(max_length=10,choices=USER_TYPE_CHOICES)