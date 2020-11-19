from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView)
from .models import Post, Team, PlayerList, Match, Stats
from plotly.graph_objs import Scatter, Figure, Bar, Pie, Sunburst
from plotly.offline import plot
# from django.http import HttpResponse


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


"""""""""
def feedback(request):
    context = {
        'posts': Post.objects.all(),
        'title': 'Feedback',
    }
    return render(request, 'main/feedback.html', context)
"""""""""


# --------------------------------------- FEEDBACK VIEWS ---------------------------------------------------------------
class PostListView(ListView):
    model = Post
    template_name = 'main/feedback.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # Prevents non-author from editing post
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/feedback/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


# --------------------------------------- COACH VIEWS ------------------------------------------------------------------
def coach_dashboard(request):
    
    return render(request, 'main/coach_dashboard.html', {'title': 'Dashboard'})


def invite_players(request):
    return render(request, 'main/invite_players.html', {'title': 'Invite Players'})


def enter_game(request):
    return render(request, 'main/enter_game.html', {'title': 'Game Entry'})


def game_list(request):
    return render(request, 'main/game_list.html', {'title': 'Games'})


# --------------------------------------- Player VIEWS -----------------------------------------------------------------
def player_dashboard(request):
    return render(request, 'main/player_dashboard.html', {'title': 'Dashboard'})


def season_stats(request):
    return render(request, 'main/season_stats.html', {'title': 'Season Stats'})


def team_comparison(request):
    return render(request, 'main/team_comparison.html', {'title': 'Team Comparison'})
