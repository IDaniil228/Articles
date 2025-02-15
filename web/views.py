from django.shortcuts import render
from django.http import HttpResponse

from web.forms import RegistrationForm
from web.models import CustomUser


def main_view(request):
    integer = 10
    return render(request, "web/main.html", {
        "int" : integer
    })

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
    return render(request, "web/registration.html", {
        "form" : form
    })