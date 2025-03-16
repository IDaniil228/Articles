from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from api.views import test_view, articles_view

urlpatterns = [
    path('', test_view),
    path('articles/', articles_view),
    path('token/', obtain_auth_token)
]