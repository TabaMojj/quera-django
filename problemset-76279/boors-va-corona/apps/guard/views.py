from django.core.cache import cache

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .utils import get_client_ip

__all__ = ('IpInfoAPIView',)


class IpInfoAPIView(GenericAPIView):

    def get(self, request):
        ip = get_client_ip(request)

        data = cache.get(ip)

        return Response(data={'info': data},
                        status=status.HTTP_200_OK)
