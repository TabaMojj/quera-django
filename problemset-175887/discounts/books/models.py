from decimal import Decimal

from django.db import models
from django.core.validators import MinValueValidator

from authors.models import Author
from discounts.models import CountryDiscount, AuthorDiscount, CategoryDiscount, BookDiscount


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
        if user and user.is_authenticated:
            country_discount = CountryDiscount.objects.filter(country=user.country)
            country_discount_percent = country_discount.get().percent if country_discount.exists() else 0
        else:
            country_discount_percent = 0

        author_discount = AuthorDiscount.objects.filter(author__in=self.authors.all())
        category_discount = CategoryDiscount.objects.filter(category__in=self.categories.all())
        book_discount = BookDiscount.objects.filter(book=self)

        author_discount_percent = author_discount.order_by('-percent').first().percent if author_discount.exists() else 0
        category_discount_percent = category_discount.order_by('-percent').first().percent if category_discount.exists() else 0
        book_discount_percent = book_discount.get().percent if book_discount.exists() else 0

        maximum_discount_percent = max(country_discount_percent, author_discount_percent, category_discount_percent, book_discount_percent)
        price_after_discount = self.price - (self.price * maximum_discount_percent / 100)
        return Decimal(price_after_discount)
