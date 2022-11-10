from django.contrib.auth.models import AbstractUser
from django.db import models
from pkg_resources import require

class User(AbstractUser):
    nickname = models.CharField(max_length=10)
    first_name = None