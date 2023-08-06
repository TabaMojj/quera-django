from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError
from django.core.validators import validate_email
from career.models import Company
from career.utils import PhoneValidator


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('current name', type=str)
        parser.add_argument('--name', type=str)
        parser.add_argument('--email', type=str)
        parser.add_argument('--phone', type=str)
        parser.add_argument('--description', type=str)

    def handle(self, *args, **options):
        current_name = options.get('current name')
        name = options.get('name')
        email = options.get('email')
        phone = options.get('phone')
        description = options.get('description')

        try:
            company = Company.objects.get(name=current_name)
        except Company.DoesNotExist:
            raise CommandError('Company matching query does not exist.')

        if name is not None:
            if not name:
                raise CommandError('Name cannot be blank.')
            elif len(name) > 50:
                raise CommandError(f'Error: Ensure this value has at most 50 characters (it has {len(name)}).')
            else:
                try:
                    Company.objects.get(name=name)
                except Company.DoesNotExist:
                    company.name = name
                else:
                    raise CommandError('Error: That name is already taken.')

        if email is not None:
            if not email:
                raise CommandError('Email cannot be blank.')
            else:
                try:
                    validate_email(email)
                except ValidationError:
                    raise CommandError('Error: Enter a valid email address.')
                else:
                    company.email = email

        if phone is not None:
            if not phone:
                raise CommandError('Phone cannot be blank.')
            else:
                try:
                    PhoneValidator(phone)
                except ValidationError:
                    raise CommandError('Error: Phone number format is not valid.')
                else:
                    company.phone = phone

        if description:
            company.description = description
        company.save()
