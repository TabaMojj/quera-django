from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Count, F
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Movie, Seat, Ticket


def list_movies(request):
    return render(request, 'app/movies.html', {
        'movies': Movie.objects.all()
    })


def list_seats(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    seats = Seat.objects.exclude(ticket__movie_id=movie.id)
    return render(request, 'app/seats.html', {
        'movie': movie,
        'seats': seats
    })


def reserve_seat(request, movie_id, seat_id):
    if request.user.is_authenticated:
        Ticket.objects.create(movie_id=movie_id, user=request.user, seat_id=seat_id)
        return redirect('list_seats', movie_id=movie_id)
    else:
        next_url = reverse('list_seats', args=[movie_id])
        return redirect(f'/login/?next={next_url}')


def stats(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden()
    number_of_reserved_for_each_seat = list(Seat.objects
                                            .values(seat__number=F('number'))
                                            .annotate(total=Count('ticket__movie')))
    return JsonResponse({'stats': number_of_reserved_for_each_seat})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('list_movies')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
