from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate

from .forms import RegisterForm, LoginForm


def login_user(request: HttpRequest):
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(
                request,
                username=username,
                password=password,
            )

            if user is not None:
                login(request, user)
                return redirect("user_profile", "me")
            else:
                return render(request, "login.html", {"form": form})
        else:
            return render(request, "login.html", {"form": form})
    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})


def register(request: HttpRequest):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            return redirect("user_profile", "me")
        else:
            print(form.is_valid())
            return render(request, "register.html", {"form": form})
    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})


def logout(request: HttpRequest):
    return render(request, "logout.html")
