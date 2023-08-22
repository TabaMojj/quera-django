from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator

from django_countries.fields import CountryField


class User(AbstractUser):
    country = CountryField(blank_label='select country', null=True, blank=True)
    wallet = models.DecimalField(default=0.00, max_digits=10, decimal_places=2, validators=[MinValueValidator(0.00)])
