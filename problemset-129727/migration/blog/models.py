from django.conf import settings
from django.db import models
from django.utils import timezone


class Category(models.Model):
    title = models.CharField(max_length=50)
    status = models.BooleanField(default=True)


class Article(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'd', 'draft'
        PUBLISH = 'p', 'publish'

    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='articles', on_delete=models.CASCADE, db_column='author', to_field='username')
    title = models.CharField(max_length=100)
    category = models.ForeignKey(Category,  related_name='articles', null=True, on_delete=models.SET_NULL, db_column='category')
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(null=True, auto_now=True)
    published = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=1, default=Status.DRAFT, choices=Status.choices)
