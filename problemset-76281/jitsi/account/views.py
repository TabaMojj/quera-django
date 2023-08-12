from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET, require_http_methods

from .models import Account, Team
from .forms import SignUpForm, LoginForm, TeamForm


@require_GET
def home(request):
    team = (Account.objects
            .filter(username=request.user)
            .values_list('team__name', flat=True)
            .get())
    return render(request, 'home.html', {'team': team})


@require_http_methods(['GET', 'POST'])
def signup(request):
    if request.method == 'GET':
        form = SignUpForm()
        return render(request, 'signup.html', {'form': form})
    else:
        form = SignUpForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            username = cd['username']
            password = cd['password1']
            form.save()
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('team')
        else:
            return redirect('signup')


@require_http_methods(['GET', 'POST'])
def login_account(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            username = cd['username']
            password = cd['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')
            else:
                return redirect('login')
        return redirect('login')


@require_GET
def logout_account(request):
    logout(request)
    return redirect('login')


@require_http_methods(['GET', 'POST'])
@login_required
def joinoradd_team(request):
    if request.method == 'GET':
        team = Account.objects.select_related('team').get(username=request.user).team
        if team:
            return redirect('home')
        else:
            form = TeamForm()
            return redirect('team', {'form': form})
    else:
        form = TeamForm(request.POST)
        if form.is_valid():
            user = request.user
            team_name = form.cleaned_data['name']
            user.team, created = Team.objects.get_or_create(name=team_name, jitsi_url_path=f'http://meet.jit.si/{team_name}')
            user.save()
            return redirect('home')
        else:
            return redirect('home')


@require_GET
def exit_team(request):
    user = Account.objects.select_related('team').get(username=request.user)
    if user.team:
        user.team = None
        user.save()
    return redirect('home')
