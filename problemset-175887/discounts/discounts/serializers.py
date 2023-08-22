from rest_framework import serializers

from .models import CountryDiscount, AuthorDiscount, CategoryDiscount


class CountryDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = CountryDiscount
        fields = '__all__'
        read_only_fields = ('id',)


class AuthorDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthorDiscount
        fields = '__all__'
        read_only_fields = ('id',)


class CategoryDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryDiscount
        fields = '__all__'
        read_only_fields = ('id',)
