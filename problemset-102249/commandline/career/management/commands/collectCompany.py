import csv
from django.conf import settings
from django.core.management.base import BaseCommand
from career.models import Company


class Command(BaseCommand):
    def handle(self, *args, **options):
        path = f'{settings.BASE_DIR}/company.csv'
        with open(path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for obj in Company.objects.all():
                row = [obj.name, obj.email, obj.phone]
                writer.writerow(row)
