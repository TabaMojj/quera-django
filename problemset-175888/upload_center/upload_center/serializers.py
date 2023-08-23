from rest_framework import serializers


class UploadFilesSerializer(serializers.Serializer):
    file_field = ...
