from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return HttpResponse('<h1>This is the home page</h1>')


def news(request):
    return HttpResponse('<h1>This is the news page</h1>')


def about(request):
    return HttpResponse('<h1>This is the about page</h1>')


def my_stats(request):
    return HttpResponse('<h1>This is the my_stats page</h1>')


def clients(request):
    return HttpResponse('<h1>This is the clients page</h1>')

