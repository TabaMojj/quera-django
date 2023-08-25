import os
import uuid

from django.conf import settings
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import MultiPartParser, FileUploadParser
from rest_framework.response import Response
from django.http.response import FileResponse
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from .serializers import UploadFilesSerializer, UserSerializer, get_megabytes, printknapSack
from django.core.files.storage import default_storage
from pathlib import Path


class UploadFile(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UploadFilesSerializer
    parser_classes = [MultiPartParser]

    def put(self, request):
        serializer = UploadFilesSerializer(data=request.data) # context={'user': request.user}
        if serializer.is_valid(raise_exception=False):

            files = serializer.validated_data['file_field']
            user = request.user
            saved_files_result = {}

            # uploaded_files_names = [file.name for file in files]
            # jjson = {}
            # for name in uploaded_files_names:
            #     if name in jjson:
            #         jjson[name] += 1
            #     else:
            #         jjson[name] = 1
            #
            # for file in files:
            #     if jjson[file.name] > 1:
            #         jjson[file.name] -= 1
            #         path = Path(file.name)
            #         file.name = path.with_name(path.stem + '-' + str(uuid.uuid4()) + path.suffix).name
            # files_permitted_to_upload = []
            # for file in files:
            #     if file.size > user.account.max_file_transfer:
            #         user_max_file_transfer_megabytes = get_megabytes(user.account.max_file_transfer)
            #         message = f'You can\'t upload files more than {user_max_file_transfer_megabytes} Megabytes!'
            #         saved_files_result[file.name] = message
            #     else:
            #         files_permitted_to_upload.append(file)

            # user_current_available_storage = user.account.storage - user.used_storage
            # files_to_upload = []
            # current_storage_used = 0
            files_permitted_to_upload_sorted = sorted(files, key=lambda x: x.size, reverse=False)

            # for file in files_permitted_to_upload_sorted:
            #     if current_storage_used + file.size <= user_current_available_storage:
            #         current_storage_used += file.size
            #         files_to_upload.append(file)
            #     else:
            #         message = 'You don\'t have enough space to upload this file!'
            #         saved_files_result[file.name] = message
            #
            # files_to_upload = printknapSack(user_current_available_storage, files_permitted_to_upload)

            # for f in files_to_upload:
            #     print(f.size)
            # for f in files_to_upload:
            #     if f in files_permitted_to_upload:
            #         files_permitted_to_upload.remove(f)
            # for f in files_permitted_to_upload:
            #     message = 'You don\'t have enough space to upload this file!'
            #     saved_files_result[f.name] = message
            for file in files_permitted_to_upload_sorted:
                if file.size > user.account.max_file_transfer:
                    user_max_file_transfer_megabytes = get_megabytes(user.account.max_file_transfer)
                    message = f'You can\'t upload files more than {user_max_file_transfer_megabytes} Megabytes!'
                    saved_files_result[file.name] = message
                    continue
                if file.size + user.used_storage > user.account.storage:
                    message = 'You don\'t have enough space to upload this file!'
                    saved_files_result[file.name] = message
                    continue
                if file.name in saved_files_result:
                    path = Path(file.name)
                    file.name = path.with_name(path.stem + '-' + str(uuid.uuid4()) + path.suffix).name

                # if file.name in saved_files_result:
                #     path = Path(file.name)
                #     file.name = path.with_name(path.stem + '-' + str(uuid.uuid4()) + path.suffix).name
                # if file.size + user.used_storage >= user.account.storage:
                #     message = 'You don\'t have enough space to upload this file!'
                #     saved_files_result[file.name] = message
                #     continue
                save = os.path.join(settings.BASE_DIR, settings.MEDIA_ROOT, user.username, file.name)
                filepath = default_storage.save(save, file)
                filename = filepath.split('/')[1]
                user.used_storage += file.size
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
