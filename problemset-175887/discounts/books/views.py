from rest_framework.viewsets import ModelViewSet

from .models import Book, Category
from .serializers import CategorySerializer


class BookViewSet(ModelViewSet):
    pass


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'pk'
