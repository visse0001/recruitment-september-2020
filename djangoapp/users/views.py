from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.http import HttpResponse
from .forms import RegisterForm, LoginForm


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()

            context = {'form': form}

            return render(request, "users/login.html", context)

    if request.method == "GET":
        form = RegisterForm()

        context = {'form': form}

        return render(request, "users/register.html", context)


def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # Load the profil
            user.first_name = form.cleaned_data.get('first_name')
            # user -> authenticate by requests to fastapiapp localhost:8000
            # if response from fastapiapp is 'PASS'
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']

            context = {"first_name": first_name,
                       "last_name": last_name,
                       "email": email
                       }

            return HttpResponse(f'{context}')
        else:
            return HttpResponse('Invalid login.')

    if request.method == "GET":
        form = LoginForm()

        return render(request, "users/login.html", {"form": form})
