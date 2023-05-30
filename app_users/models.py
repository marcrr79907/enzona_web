from typing import Iterable, Optional
from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    ci = models.CharField(max_length=200, unique=True, null=True)
    phone = models.IntegerField(unique=True, null=True)
