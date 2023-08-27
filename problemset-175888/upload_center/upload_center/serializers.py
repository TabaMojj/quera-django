from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.core.files.storage import default_storage

User = get_user_model()


def get_megabytes(value):
    megabytes = value / (1024 * 1024)
    value = f'{megabytes:.3f}'
    return value


class UploadFilesSerializer(serializers.Serializer):
    file_field = serializers.FileField(allow_empty_file=False, allow_null=False)

    # file_field = serializers.ListField(
    #     child=serializers.FileField(allow_empty_file=False, allow_null=False),
    #     allow_null=False, allow_empty=False)

    def validate(self, attrs):
        super().validate(attrs)
        attrs = self.initial_data.getlist('file_field')
        for file in attrs:
            if file.size == 0:
                raise serializers.ValidationError('Empty File')
        return self.initial_data.getlist('file_field')


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
        if default_storage.exists(name=username):
            user_files = default_storage.listdir(path=username)[1]
            if user_files:
                return user_files
        return f'{username} doesn\'t have any files!'
