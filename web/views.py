from django.shortcuts import render
from django.http import HttpResponse

def main_view(response):
    integer = 10
    return render(response, "web/main.html", {
        "int" : integer
    })