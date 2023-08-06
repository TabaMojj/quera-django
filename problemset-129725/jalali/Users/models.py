from django.db import models
from django_jalali.db import models as jmodels
import jdatetime
from django.core.validators import RegexValidator

FullNameValidator = RegexValidator(
    regex=r'^[A-Z][a-zA-Z]{3,} [A-Z][a-zA-Z]{3,}$',
    message='Full name is not correct.',
)

NationalCodeValidator = RegexValidator(
    regex=r'^\d{10}$',
    message='National Code must be 10 characters.'
)


class CustomUser(models.Model):
    class Gender(models.TextChoices):
        MALE = 'M', 'Male'
        FEMALE = 'F', 'Female'

    username = models.CharField(max_length=256)
    full_name = models.CharField(max_length=256, validators=[FullNameValidator])
    gender = models.CharField(max_length=1, choices=Gender.choices)
    national_code = models.CharField(max_length=10, validators=[NationalCodeValidator])
    birthday_date = jmodels.jDateField()
    ceremony_datetime = jmodels.jDateTimeField()
    country = models.CharField(max_length=4, default='Iran', editable=False)

    def get_first_and_last_name(self):
        first_name, last_name = self.full_name.split()
        return {'first_name': first_name, 'last_name': last_name}

    def get_age(self):
        today = jdatetime.date.today()
        age = today.year - self.birthday_date.year
        if today.month < self.birthday_date.month or (
                today.month == self.birthday_date.month and today.day < self.birthday_date.day):
            age -= 1
        return age

    def is_birthday(self):
        today = jdatetime.date.today()
        return today.month == self.birthday_date.month and today.day == self.birthday_date.day
