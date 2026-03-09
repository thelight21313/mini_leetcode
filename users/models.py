from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    avatar = models.URLField(blank=True, null=True)
    rating = models.IntegerField(default=0)
    bio = models.TextField(blank=True)


