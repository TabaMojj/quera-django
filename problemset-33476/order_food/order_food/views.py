from django.dispatch import receiver
from django.shortcuts import render
from django.contrib import messages
from .models import Food
from django_comments.signals import comment_was_posted


@receiver(comment_was_posted)
def comment_posted(request, **kwargs):
    messages.success(request, "your comment successfully submitted.")


def menu_view(request):
    foods = Food.objects.all()
    return render(request, 'order_food/menu.html', {
        'foods': foods,
        'user': request.user
    })
