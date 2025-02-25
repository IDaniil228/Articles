from collections import defaultdict

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import HttpResponse

from web.forms import RegistrationForm, AuthorizationForm, ArticlesForm
from web.models import CustomUser, Articles


def main_view(request):
    if not request.user.is_anonymous:
        articles = Articles.objects.filter(user=request.user)
        subscriptions = request.user.subscriptions.all()
        return render(request, "web/main.html", {
            "articles" : articles,
            "subscriptions" : subscriptions
        })
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


def logout_view(request):
    logout(request)
    return redirect("main")


def articles_view(request, id = None):
    articles = Articles.objects.get(id=id) if id is not None else None
    form = ArticlesForm(instance=articles)
    if request.method == "POST":
        form = ArticlesForm(data=request.POST, files=request.FILES, instance=articles, initial={"user" : request.user})
        if form.is_valid():
            form.save()
            return redirect("main")
    return render(request, "web/articles.html", {
        "form" : form
    })

def viewing_articles_view(request, id):
    article = Articles.objects.get(id=id)
    return render(request, "web/viewing_articels.html", {
        "article" : article
    })

def other_authors_view(request):
    all_sub_id = list(request.user.subscriptions.values_list('id', flat=True))
    all_users = CustomUser.objects.exclude(id__in=all_sub_id).exclude(id=request.user.id)
    return render(request, "web/other_authors.html", {
        "users" : all_users
    })

def check_profile_view(request, id):
    user = CustomUser.objects.get(id=id)
    articles = Articles.objects.filter(user=user)
    print(articles)
    return render(request, "web/check_profile.html", {
        "user" : user,
        "articles" : articles
    })


def subscribe_view(request, id):
    user = CustomUser.objects.get(id=id)
    request.user.subscriptions.add(user)
    return redirect("other_authors")