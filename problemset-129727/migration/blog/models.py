from django.db import models


class Article(models.Model):
    author = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
