from django.urls import path, include
from rest_framework import routers

from .views import CountryDiscountViewSet, AuthorDiscountViewSet, CategoryDiscountViewSet

app_name = 'discounts'

router = routers.SimpleRouter()
router.register('country-discounts', CountryDiscountViewSet, basename='country-discounts')
router.register('author-discounts', AuthorDiscountViewSet, basename='author-discounts')
router.register('category-discounts', CategoryDiscountViewSet, basename='category-discounts')

urlpatterns = [
    path('', include(router.urls)),
]
