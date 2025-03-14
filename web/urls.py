from django.contrib import admin
from django.urls import path
from web.views import *

urlpatterns = [
    path('', main_view, name="main"),
    path('registration/', registration_view, name="registration"),
    path('edit/', edit_profile_view, name="edit_profile"),
    path('auth/', auth_view, name="auth"),
    path('logout/', logout_view, name="logout"),
    path('articles/create', articles_view, name="articles_create"),
    path('tags/create/', tags_view, name="create_tags"),
    path('tags/delete/<int:id>', tags_delete_view, name="delete_tag"),
    path('articles/<int:id>', articles_view, name="articles_edit"),
    path('articles/view/<int:id>', viewing_articles_view, name="articles_view"),
    path('other_authors/', other_authors_view, name="other_authors"),
    path('other_authors/<int:id>', check_profile_view, name="check_profile"),
    path('other_authors/<int:id>/subscribe', subscribe_view, name="subscribe"),
    path('import/', import_view, name="import")
]