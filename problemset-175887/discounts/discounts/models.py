from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator

from django_countries.fields import CountryField


class GeneralDiscount(models.Model):
    percent = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CountryDiscount(GeneralDiscount):
    country = CountryField(blank_label='select country', unique=True)


class AuthorDiscount(GeneralDiscount):
    author = models.OneToOneField('authors.Author', on_delete=models.CASCADE, unique=True)


class CategoryDiscount(GeneralDiscount):
    category = models.OneToOneField('books.Category', on_delete=models.CASCADE, unique=True)


class BookDiscount(GeneralDiscount):
    book = models.OneToOneField('books.Book', on_delete=models.CASCADE, unique=True)
