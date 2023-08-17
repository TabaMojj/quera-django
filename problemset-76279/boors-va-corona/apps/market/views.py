from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status

__all__ = ('IndexAPIView',)


class IndexAPIView(GenericAPIView):

    def get(self, request):
        return Response(data={'market': 'This is our main market'},
                        status=status.HTTP_200_OK)
