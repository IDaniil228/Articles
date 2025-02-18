from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import HttpResponse

from web.forms import RegistrationForm, AuthorizationForm
from web.models import CustomUser


def main_view(request):
    return render(request, "web/main.html")

def registration_view(request):
    form = RegistrationForm()
    if request.method == "POST":
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            user = CustomUser(
                login = form.cleaned_data['login'],
                name = form.cleaned_data['name'],
                surname = form.cleaned_data['surname']
            )
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect("main")
    return render(request, "web/registration.html", {
        "form" : form
    })

def auth_view(request):
    form = AuthorizationForm()
    if request.method == "POST":
        form = AuthorizationForm(data=request.POST)
        if form.is_valid():
            user = authenticate(**form.cleaned_data)
            if user is None:
                form.add_error(None, "Неверный логин или пароль")
            else:
                login(request, user)
                return redirect("main", permanent=True)
    return render(request, "web/authorization.html", {
        "form" : form
    })