import os
import uuid
from _decimal import Decimal
from pathlib import Path

from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.core.files.storage import default_storage
from rest_framework.exceptions import ValidationError
import decimal

User = get_user_model()


def get_megabytes(value): #TODO: WRITE ABOUT THIS IN README
    megabytes = value / (1024 * 1024)
    value = f'{megabytes:.3f}'
    return value


def printknapSack(user_available_storage, files):
    chosen_files = []
    user_available_storage = int(float(get_megabytes(user_available_storage)))
    n = len(files)
    val = [1] * n
    K = [[0 for w in range(user_available_storage + 1)]
         for i in range(n + 1)]
    for i in range(n + 1):
        for w in range(user_available_storage + 1):
            if i == 0 or w == 0:
                K[i][w] = 0
            elif int(float(get_megabytes(files[i - 1].size))) <= w:
                K[i][w] = max(val[i - 1]
                              + K[i - 1][w - int(float(get_megabytes(files[i - 1].size)))],
                              K[i - 1][w])
            else:
                K[i][w] = K[i - 1][w]
    res = K[n][user_available_storage]
    w = user_available_storage
    for i in range(n, 0, -1):
        if res <= 0:
            break
        if res == K[i - 1][w]:
            continue
        else:
            chosen_files.append(files[i - 1])
            res = res - val[i - 1]
            w = w - int(float(get_megabytes(files[i - 1].size)))
    return chosen_files





class UploadFilesSerializer(serializers.Serializer):
    # file_field = serializers.FileField(allow_empty_file=False, required=True, use_url=False)
    #
    file_field = serializers.ListField(
        child=serializers.FileField(use_url=False, allow_empty_file=False, allow_null=False),
        allow_null=False, allow_empty=False)

    # def create(self, validated_data):
    #     user = self.context['user']
    #     files = validated_data['file_field']
    #     saved_files_result = {}
    #     number_of_files = len(files)
    #     if number_of_files == 1 and files[0].size == 0:
    #         raise ValidationError('EMPTY !!')
    #
    #     uploaded_files_names = [file.name for file in files]
    #     jjson = {}
    #     for name in uploaded_files_names:
    #         if name in jjson:
    #             jjson[name] += 1
    #         else:
    #             jjson[name] = 1
    #
    #     for file in files:
    #         if jjson[file.name] > 1:
    #             jjson[file.name] -= 1
    #             path = Path(file.name)
    #             file.name = path.with_name(path.stem + '-' + str(uuid.uuid4()) + path.suffix).name
    #     files_permitted_to_upload = []
    #     for file in files:
    #         if file.size > user.account.max_file_transfer:
    #             user_max_file_transfer_megabytes = get_megabytes(user.account.max_file_transfer)
    #             message = f'You can\'t upload files more than {user_max_file_transfer_megabytes} Megabytes!'
    #             saved_files_result[file.name] = message
    #         else:
    #             files_permitted_to_upload.append(file)
    #
    #     user_current_available_storage = user.account.storage - user.used_storage
    #     files_to_upload = printknapSack(user_current_available_storage, files_permitted_to_upload)
    #     for f in files_to_upload:
    #         if f in files_permitted_to_upload:
    #             files_permitted_to_upload.remove(f)
    #     for f in files_permitted_to_upload:
    #         message = 'You don\'t have enough space to upload this file!'
    #         saved_files_result[f.name] = message
    #     for file in files_to_upload:
    #         if file.size == 0:
    #             continue
    #         # file_directory = default_storage.generate_filename(f'{user.username}/{file.name}')
    #         # filename = file_directory.split('/')[1]
    #
    #         save = os.path.join(settings.BASE_DIR, settings.MEDIA_ROOT, user.username, file.name)
    #         filepath = default_storage.save(save, file.file)
    #         filename = filepath.split('/')[1]
    #         user.used_storage += file.size
    #         user.save()
    #         url = default_storage.url(filepath)
    #         saved_files_result[filename] = url
    #     return saved_files_result

    # def save(self, **kwargs):
    # user = self.context['user']
    # files = self.validated_data['file_field']
    # saved_files_result = {}
    # number_of_files = len(files)
    # if number_of_files == 1 and files[0].size == 0:
    #     raise ValidationError('EMPTY !!')
    #
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
    #
    # user_current_available_storage = user.account.storage - user.used_storage
    # files_to_upload = printknapSack(user_current_available_storage, files_permitted_to_upload)
    # for f in files_to_upload:
    #     if f in files_permitted_to_upload:
    #         files_permitted_to_upload.remove(f)
    # for f in files_permitted_to_upload:
    #     message = 'You don\'t have enough space to upload this file!'
    #     saved_files_result[f.name] = message
    # for file in files_to_upload:
    #     if file.size == 0:
    #         continue
    #     # file_directory = default_storage.generate_filename(f'{user.username}/{file.name}')
    #     # filename = file_directory.split('/')[1]
    #
    #     save = os.path.join(settings.BASE_DIR, settings.MEDIA_ROOT, user.username, file.name)
    #     print(save)
    #     filepath = default_storage.save(save, file.file)
    #     filename = filepath.split('/')[1]
    #     user.used_storage += file.size
    #     user.save()
    #     url = default_storage.url(filepath)
    #     saved_files_result[filename] = url
    # return saved_files_result


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('Account', 'Storage', 'Used', 'Files')

    Account = serializers.CharField(source='account.title', read_only=True)
    Storage = serializers.SerializerMethodField(method_name='get_storage', read_only=True)
    Used = serializers.SerializerMethodField(method_name='get_used', read_only=True)
    Files = serializers.SerializerMethodField(method_name='get_files', read_only=True)

    def get_storage(self, obj):
        return get_megabytes(obj.account.storage)

    def get_used(self, obj):
        return get_megabytes(obj.used_storage)

    def get_files(self, obj):
        username = obj.username
        is_username_folder_exists = default_storage.exists(name=username)
        if is_username_folder_exists:
            user_files = default_storage.listdir(path=username)[1]
            if user_files:
                return user_files
        return f'{username} doesn\'t have any files!'
