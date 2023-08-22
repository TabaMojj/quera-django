

from decimal import Decimal

from django.db import models
from django.core.validators import MinValueValidator

from authors.models import Author


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class Book(models.Model):
    isbn = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    content = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0.00)])
    authors = models.ManyToManyField(Author)
    categories = models.ManyToManyField(Category, blank=True)

    def __str__(self):
        return self.title

    def get_discount(self, user=None) -> Decimal:
        pass
