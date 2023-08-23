from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


# Create your views here.
class RevokeTokenView(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request, *args, **kwargs):
        request.auth.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
