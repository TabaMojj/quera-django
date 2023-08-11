from django.db.models import F
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from .models import OrderItem, Order


def checkout(request, order_pk):
    order = get_object_or_404(Order, pk=order_pk)
    total_price = (OrderItem.objects
                   .filter(order=order)
                   .annotate(sum_price=F('quantity') * F('product__price'))
                   .aggregate(total_price=Sum('sum_price')))
    return JsonResponse(total_price)
