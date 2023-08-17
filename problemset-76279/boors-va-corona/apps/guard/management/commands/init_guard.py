from django.core.management.base import BaseCommand

from ...models import SecurityConfig, ViewDetail
from ...utils import list_views


class Command(BaseCommand):
    """ This command initializes the gurad
        for enhancing the security of your project.
    """
    help = 'Initialize Guard app'

    def handle(self, *args, **options):
        views = []
        if not ViewDetail.objects.exists():
            for path, name in list_views():
                view = ViewDetail.objects.create(name=name, path=path)
                views.append(view)

        if not SecurityConfig.objects.exists():
            config = SecurityConfig.objects.create()
            for view in views:
                config.views.add(view)
