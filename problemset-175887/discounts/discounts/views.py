from rest_framework.viewsets import ModelViewSet

from .models import CountryDiscount, AuthorDiscount, CategoryDiscount
from .serializers import CountryDiscountSerializer, AuthorDiscountSerializer, CategoryDiscountSerializer
from .permissions import IsSuperUser


class CountryDiscountViewSet(ModelViewSet):
    """
    API endpoint that allows discounts to be viewed or edited.
    """
    queryset = CountryDiscount.objects.all()
    serializer_class = CountryDiscountSerializer
    permission_classes = (IsSuperUser,)


class AuthorDiscountViewSet(ModelViewSet):
    """
    API endpoint that allows discounts to be viewed or edited.
    """
    queryset = AuthorDiscount.objects.all()
    serializer_class = AuthorDiscountSerializer
    permission_classes = (IsSuperUser,)


class CategoryDiscountViewSet(ModelViewSet):
    """
    API endpoint that allows discounts to be viewed or edited.
    """
    queryset = CategoryDiscount.objects.all()
    serializer_class = CategoryDiscountSerializer
    permission_classes = (IsSuperUser,)
