from django.contrib.auth.models import AbstractUser
from django.db import models
from pkg_resources import require

class User(AbstractUser):
    followings = models.ManyToManyField("self", symmetrical=False, related_name="followers")
    nickname = models.CharField(max_length=10, unique=True)
    first_name = None