import os
import uuid

from django.conf import settings
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from django.http.response import FileResponse
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from .serializers import UploadFilesSerializer, UserSerializer, get_megabytes
from django.core.files.storage import default_storage
from pathlib import Path


class UploadFile(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UploadFilesSerializer
    parser_classes = [MultiPartParser]

    def put(self, request):
        serializer = UploadFilesSerializer(data=request.data)
        if serializer.is_valid(raise_exception=False):
            files = serializer.validated_data['file_field']
            user = request.user
            saved_files_result = {}
            max_file_transfer_message = f'You can\'t upload files more than {get_megabytes(user.account.max_file_transfer)} Megabytes!'
            not_enough_storage_message = 'You don\'t have enough space to upload this file!'
            can_upload = sorted(files, key=lambda x: x.size)
            for file in can_upload:
                if file.name in saved_files_result:
                    path = Path(file.name)
                    file.name = path.with_name(path.stem + '-' + str(uuid.uuid4()) + path.suffix).name
                save = os.path.join(settings.BASE_DIR, settings.MEDIA_ROOT, user.username, file.name)
                filepath = default_storage.save(save, file)
                filename = filepath.split('/')[1]
                user.used_storage = user.used_storage + file.size
                user.save()
                url = default_storage.url(filepath)
                saved_files_result[filename] = url
            return Response(saved_files_result)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FileManager(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get(self, request):
        serializer = UserSerializer(request.user, many=False)
        return Response(serializer.data)

    def delete(self, request):

        file_name = request.POST.get('file_name')
        if not file_name:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        file_location = os.path.join(settings.BASE_DIR, settings.MEDIA_ROOT, request.user.username, file_name)
        if default_storage.exists(file_location):
            file_size = default_storage.size(file_location)
            default_storage.delete(file_location)
            request.user.used_storage -= file_size
            request.user.save()
            return Response({'detail': f'{file_name} Deleted Successfully.'})
        else:
            return Response({"detail": f"{file_name} hasn't existed!"}, status=status.HTTP_404_NOT_FOUND)


class DownloadFile(GenericAPIView):
    permission_classes = (AllowAny,)

    def get(self, request, user, filename):
        file_location = os.path.join(settings.BASE_DIR, settings.MEDIA_ROOT, user, filename)
        if default_storage.exists(file_location):
            return FileResponse(default_storage.open(file_location))
        else:
            return Response({"detail": f"{filename} hasn't existed!"}, status=status.HTTP_404_NOT_FOUND)
