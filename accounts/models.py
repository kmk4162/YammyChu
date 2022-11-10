from django.contrib.auth.models import AbstractUser
from django.db import models
from pkg_resources import require
from articles.models import Team
class User(AbstractUser):
    nickname = models.CharField(max_length=10, unique=True)
    first_name = None
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True)
    