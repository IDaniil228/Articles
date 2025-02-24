from django.contrib import admin
from django.urls import path
from web.views import *

urlpatterns = [
    path('', main_view, name="main"),
    path('registration/', registration_view, name="registration"),
    path('auth/', auth_view, name="auth"),
    path('logout/', logout_view, name="logout"),
    path('articles/create', articles_view, name="articles_create"),
    path('articles/<int:id>', articles_view, name="articles_edit"),
    path('articles/view/<int:id>', viewing_articles, name="articles_view")
]