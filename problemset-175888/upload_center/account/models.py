from django.db import models

from django.contrib.auth.models import AbstractUser


class Account(models.Model):
    title = models.CharField(max_length=50, unique=True)
    storage = models.PositiveIntegerField()  # Bytes
    max_file_transfer = models.PositiveSmallIntegerField()  # Bytes


class User(AbstractUser):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    used_storage = models.PositiveSmallIntegerField(default=0)