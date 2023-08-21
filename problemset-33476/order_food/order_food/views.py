from django.shortcuts import render
from order_food.models import *


def menu_view(request):
    foods = Food.objects.all()
    return render(request, 'order_food/menu.html', {
        'foods': foods,
    })
