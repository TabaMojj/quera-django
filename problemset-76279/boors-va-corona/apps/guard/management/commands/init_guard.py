from django.core.management.base import BaseCommand

from apps.guard.models import SecurityConfig, ViewDetail
from apps.guard.utils import list_views


class Command(BaseCommand):
    """ This command initializes the gurad
        for enhancing the security of your project.
    """
    help = 'Initialize Guard app'

    # Your code
