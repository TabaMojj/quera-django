from datetime import timedelta
from django.http import JsonResponse
from django.core.cache import cache
from django.utils import timezone
from rest_framework import status
from .models import BlockedIp, ViewDetail
from .utils import get_client_ip


class BlockIpMiddleware:
    maximum_rps = 4
    timeout = 60

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_ip = get_client_ip(request)
        path = request.path
        default_cache_value = {'count': 0, 'last_updated': timezone.now()}

        if self.banned_before(user_ip):
            return JsonResponse(data={'message': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)

        requests = cache.get(user_ip) or default_cache_value
        if self.validate_request_per_second(requests=requests, user_ip=user_ip, path=path):
            return JsonResponse({'message': 'Too many requests'}, status=status.HTTP_429_TOO_MANY_REQUESTS)

        response = self.get_response(request)
        cache.set(user_ip, requests, timeout=self.timeout)
        return response

    def banned_before(self, user_ip):
        blocked_ip = BlockedIp.objects.filter(ip=user_ip)
        if blocked_ip.exists() and blocked_ip.get().is_blocked:
            return True
        return False

    def validate_request_per_second(self, user_ip, requests, path):
        requests['count'] += 1
        requests['last_updated'] = timezone.now()
        count = requests['count']
        now = requests['last_updated']
        delta = now - timezone.now()
        if count > self.maximum_rps and delta < timedelta(seconds=1):
            view = ViewDetail.objects.get(path=path)
            BlockedIp.objects.create(ip=user_ip, view=view, rps=self.maximum_rps)
            return True
        cache.set(user_ip, requests)
        return False
