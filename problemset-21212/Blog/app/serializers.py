from rest_framework import serializers
from .models import Post, Comment


class PostSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    body = serializers.CharField()
    created = serializers.DateTimeField(read_only=True)
    owner = serializers.CharField(read_only=True)

    def create(self, validated_data):
        return Post.objects.create(**validated_data)


class PostDetailSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    body = serializers.CharField()
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)
    owner = serializers.CharField(source='owner.username', read_only=True)
    comment_set = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='comment_detail')

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.body = validated_data.get('body', instance.body)
        instance.save()
        return instance


class CommentSerializer(serializers.Serializer):
    body = serializers.CharField()
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)
    post = serializers.HyperlinkedRelatedField(view_name='post_detail', read_only=True)
    owner = serializers.CharField(source='owner.username', read_only=True)

    def create(self, validated_data):
        return Comment.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.body = validated_data.get('body', instance.body)
        instance.save()
        return instance
