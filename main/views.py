from django.shortcuts import render
from .models import Post

# from django.http import HttpResponse


posts = [
    {
        'author': 'MikeMDC',
        'title': 'new post!',
        'content': 'ha sike',
        'date_posted': 'August 27, 2018'
    },
    {
        'author': 'MikeMDC1',
        'title': 'second post!',
        'content': 'ha ddddd',
        'date_posted': 'August 27, 2019'
    },
]


def home(request):

    return render(request, 'main/home.html', {'title': 'Home'})


def news(request):
    return render(request, 'main/news.html', {'title': 'News'})


def about(request):
    return render(request, 'main/about.html', {'title': 'About'})


def my_stats(request):
    return render(request, 'main/my_stats.html', {'title': 'Stats'})


def clients(request):
    return render(request, 'main/clients.html', {'title': 'Clients'})


def feedback(request):
    context = {
        'posts': Post.objects.all(),
        'title': 'Feedback',
    }
    return render(request, 'main/feedback.html', context)
