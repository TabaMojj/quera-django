from django.core.management.base import BaseCommand
from career.models import Company


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--all', action='store_true')
        parser.add_argument('company name', nargs='*', type=str)

    def handle(self, *args, **options):
        if options['all']:
            Company.objects.all().delete()
        else:
            for company in options['company name']:
                try:
                    Company.objects.get(name=company).delete()
                except Company.DoesNotExist:
                    self.stderr.write(f'{company} matching query does not exist.')
