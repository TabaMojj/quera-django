from django.urls import path, include
from rest_framework import routers

from .views import BookViewSet, CategoryViewSet

app_name = 'books'

router = routers.SimpleRouter()
router.register('books', BookViewSet, basename='books')
router.register('category', CategoryViewSet, basename='category')

urlpatterns = [
    path('', include(router.urls)),
]
