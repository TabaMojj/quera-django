from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import Book, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')
        read_only_fields = ('id',)


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

    categories = serializers.PrimaryKeyRelatedField(many=True, queryset=Category.objects.all())
    price_after_discount = serializers.SerializerMethodField()

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        categories = representation.pop('categories')
        category_urls = [reverse('books:category-detail',
                                 kwargs={'pk': category},
                                 request=self.context['request'])
                         for category in categories]
        representation['categories'] = category_urls
        return representation

    def get_price_after_discount(self, obj):
        request = self.context.get('request')
        return obj.get_discount(request.user)
