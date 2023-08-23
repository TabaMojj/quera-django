from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from django.http.response import FileResponse
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status

from .serializers import UploadFilesSerializer

class UploadFile(GenericAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = UploadFilesSerializer

    def put(self, request):
        #Todo: Complete put function for uploading multiple files

class FileManager(GenericAPIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        #Todo: Complete get function for getting accounts status.

    def delete(self, request):
        #Todo: Complete delete function for deleting files.


class DownloadFile(GenericAPIView):
    permission_classes = (AllowAny, )

    def get(self, request, user, filename):
        #Todo: Complete get function for downloading files using FileResponse.
