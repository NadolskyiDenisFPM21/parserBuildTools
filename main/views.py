from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from sites.models import Site

from .tasks import task


@login_required(login_url='login')
def index(request):
    sites = Site.objects.all()
    context = {'sites': sites}

    return render(request, 'index.html', context)


def task_parse(request):
    sites = Site.objects.all()
    task(request, sites)

    return JsonResponse({'status': True})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль.')

    return render(request, 'login.html')
