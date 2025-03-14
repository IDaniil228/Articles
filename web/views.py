from collections import defaultdict
from gc import get_objects

from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

from web.forms import RegistrationForm, AuthorizationForm, ArticlesForm, EditProfileForm, ArticlesFilterForm, \
    ImportCSVFrom, CreateTagForm
from web.models import CustomUser, Articles, Tag
from web.services import export_articles_csv, import_csv


def main_view(request):
    if not request.user.is_anonymous:
        articles = Articles.objects.filter(user=request.user).order_by("title")

        filter_form = ArticlesFilterForm(request.GET)
        filter_form.is_valid()
        filters = filter_form.cleaned_data
        if filters["search"]:
            articles = articles.filter(title__icontains=filters["search"])

        paginator = Paginator(articles, 2)
        page_number = request.GET.get("page", 1)

        subscriptions = request.user.subscriptions.all()
        subscribers_count = len(CustomUser.objects.filter(subscriptions=request.user))

        get_params = request.GET.copy()
        if "page" in get_params:
            del get_params["page"]

        if "export" in request.GET and request.GET["export"] == "csv":
            response = HttpResponse(
                content_type="text/csv",
                headers={"Content-Disposition" : "attachment; filename=articles.csv" }
            )
            return  export_articles_csv(articles, response)

        return render(request, "web/main.html", {
            "articles" : paginator.get_page(page_number),
            "subscriptions" : subscriptions,
            "subscribers_count" : subscribers_count,
            "filter_form" : filter_form,
            "get_params" : get_params
        })
    return render(request, "web/main.html")

def registration_view(request):
    form = RegistrationForm()
    if request.method == "POST":
        form = RegistrationForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            if CustomUser.objects.filter(login=form.cleaned_data['login']):
                form.add_error("login", "Такой логин уже существует")
            else:
                    user = CustomUser(
                        login=form.cleaned_data['login'],
                        name=form.cleaned_data['name'],
                        surname=form.cleaned_data['surname'],
                        photo=form.cleaned_data['photo']
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
    article = get_object_or_404(Articles, id=id) if id is not None else None
    form = ArticlesForm(instance=article)
    if request.method == "POST":
        form = ArticlesForm(data=request.POST, files=request.FILES, instance=article, initial={"user" : request.user})
        if form.is_valid():
            form.save()
            return redirect("main")
    return render(request, "web/articles.html", {
        "form" : form
    })

def viewing_articles_view(request, id):
    article = get_object_or_404(Articles.objects.prefetch_related("tags"), id=id)
    #article = get_object_or_404(Articles, id=id)
    return render(request, "web/viewing_articels.html", {
        "article" : article,
        "tags" : article.tags.all()
    })

def other_authors_view(request):
    all_sub_id = list(request.user.subscriptions.values_list('id', flat=True))
    all_users = CustomUser.objects.exclude(id__in=all_sub_id).exclude(id=request.user.id)
    return render(request, "web/other_authors.html", {
        "users" : all_users
    })

def check_profile_view(request, id):
    sub_user = request.user.subscriptions.filter(id=id)
    already_sub = True if sub_user else False
    user = CustomUser.objects.get(id=id)
    articles = Articles.objects.filter(user=user)
    return render(request, "web/check_profile.html", {
        "user" : user,
        "articles" : articles,
        "already_sub" : already_sub
    })


def subscribe_view(request, id):
    user = get_object_or_404(CustomUser, id=id)
    request.user.subscriptions.add(user)
    return redirect("other_authors")


def edit_profile_view(request):
    form = EditProfileForm(instance=request.user)
    if request.method == "POST":
        form = EditProfileForm(data=request.POST, files=request.FILES, instance=request.user)
        form.save()
        return redirect("main")

    return render(request, "web/registration.html", {
        "form" : form
    })


def import_view(request):
    if request.method == "POST":
        form = ImportCSVFrom(files=request.FILES)
        if form.is_valid():
            import_csv(form.cleaned_data["file"], request.user)
            return redirect("main")
    return render(request, "web/import.html", {
        "form" : ImportCSVFrom()
    })


def tags_view(request):
    form = CreateTagForm()
    if request.method == "POST":
        form = CreateTagForm(data=request.POST)
        if form.is_valid():
            form.save()
    list_tags = Tag.objects.all()
    return render(request, "web/create_tag.html", {
        "form" : form,
        "list_tags" : list_tags
    })


def tags_delete_view(request, id):
    get_object_or_404(Tag, id=id).delete()
    return redirect("create_tags")