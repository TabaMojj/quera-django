from django.contrib.auth import get_user_model
from django.db.models import F
from django.http import JsonResponse
from .models import Borrowing, Book

User = get_user_model()


def get_book_users(request, book_id):
    response = list((Borrowing.objects
                     .filter(book_id=book_id)
                     .annotate(username=F('user__username'))
                     .values('username', 'date')))
    return JsonResponse(response, safe=False)


def borrow_book(request, book_id, user_name):
    is_borrowed = Book.objects.filter(id=book_id, user_borrowed__isnull=False).exists()
    if is_borrowed:
        return JsonResponse({'status': 1}, safe=True)

    user_has_borrowed = Book.objects.filter(user_borrowed__username=user_name).exists()
    if user_has_borrowed:
        return JsonResponse({'status': 2}, safe=True)

    is_user_exist = User.objects.filter(username=user_name).exists()
    is_book_exist = Book.objects.filter(id=book_id).exists()
    if not is_book_exist or not is_user_exist:
        return JsonResponse({'status': 3}, safe=True)

    try:
        user = User.objects.get(username=user_name)
        Book.objects.get(id=book_id).borrow_book(user=user)
        return JsonResponse({'status': 0}, safe=True)
    except:
        return JsonResponse({'status': 4}, safe=True)


def return_book(request, book_id):
    is_returned = Book.objects.filter(id=book_id, user_borrowed__isnull=True).exists()
    if is_returned:
        return JsonResponse({'status': 1}, safe=True)

    is_book_exist = Book.objects.filter(id=book_id).exists()
    if not is_book_exist:
        return JsonResponse({'status': 2}, safe=True)

    try:
        Book.objects.get(id=book_id).return_book()
        return JsonResponse({'status': 0}, safe=True)
    except:
        return JsonResponse({'status': 3}, safe=True)

