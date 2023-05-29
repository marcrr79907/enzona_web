from typing import Iterable, Optional
from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    ci = models.CharField(max_length=200, unique=True, null=True)
    phone = models.IntegerField(unique=True, null=True)

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.set_password(self.password)
        else:
            user = User.objects.get(pk=self.pk)
            if user.password != self.password:
                self.set_password(self.password)
        super().save(*args, **kwargs)
