from django.db import models
from django.contrib.auth.models import AbstractUser


class UserData(AbstractUser):
    phone_number = models.CharField(max_length=13)
