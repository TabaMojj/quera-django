from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand
from career.models import Company
from django.core.validators import validate_email
from career.utils import PhoneValidator


class Command(BaseCommand):
    def handle(self, *args, **options):
        while True:
            name = input('Name: ')
            if not name:
                self.stderr.write('Error: This field cannot be blank.')
            elif len(name) > 50:
                self.stderr.write(f'Error: Ensure this value has at most 50 characters (it has {len(name)}).')
            else:
                try:
                    Company.objects.get(name=name)
                except Company.DoesNotExist:
                    break
                else:
                    self.stderr.write(f'Error: That name is already taken.')

        while True:
            email = input('Email: ')
            if not email:
                self.stderr.write('Error: This field cannot be blank.')
            else:
                try:
                    validate_email(email)
                except ValidationError:
                    self.stderr.write('Error: Enter a valid email address.')
                else:
                    break

        while True:
            phone = input('Phone: ')
            if not phone:
                self.stderr.write('Error: This field cannot be blank.')
            else:
                try:
                    PhoneValidator(phone)
                except ValidationError:
                    self.stderr.write('Error: Phone number format is not valid.')
                else:
                    break

        description = input('Description: ')
        description = None if not description else description
        company = Company(name=name, phone=phone, email=email, description=description)
        company.save()
