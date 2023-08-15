from django.http import JsonResponse

from django.core.cache import cache
from django.urls import resolve
from django.utils import timezone
from rest_framework import status

from .models import BlockedIp, SecurityConfig, ViewDetail

from .utils import get_client_ip


class BlockIpMiddleware:
    maximum_rps = 4
    timeout = 60

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        view, _, _ = resolve(request.path)
        user_ip = get_client_ip(request)

        response = self.banned_before(user_ip)
        if response:
            return response

        LIMITED_VIEWS = SecurityConfig.objects.last().views.values_list(
            'name',
            flat=True)

        # Your code

        response = self.get_response(request)

        return response

        pass

    def banned_before(self, user_ip):

        # Your code
        pass

    def validate_request_per_second(self, user_ip, url_path, data):

        # Your code
        pass
