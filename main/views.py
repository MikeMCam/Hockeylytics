from django.shortcuts import render, redirect
from .models import Team, Match
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import TeamCreateForm

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


# --------------------------------------- COACH VIEWS ------------------------------------------------------------------
@login_required()
def coach_dashboard(request):
    context = {
        'title': 'Dashboard',
    }
    return render(request, 'main/coach_dashboard.html', context)


@login_required()
def invite_players(request):
    user = request.user
    teamList = Team.objects.get(coach=user)

    context = {
        'title': 'Invite Players',
        'team_list': teamList,
    }
    return render(request, 'main/invite_players.html', context)


@login_required()
def enter_game(request):
    if request.method == 'POST':
        form = TeamCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Match {form.homeTeam} vs. {form.awayTeam} has been created')
            redirect(coach_dashboard)
    else:
        form = TeamCreateForm()

    context = {
        'form': form,
        'title': 'Game Entry',
    }
    return render(request, 'main/enter_game.html', context)


@login_required()
def game_list(request):
    return render(request, 'main/game_list.html', {'title': 'Games'})


# --------------------------------------- Player VIEWS -----------------------------------------------------------------
@login_required()
def player_dashboard(request):
    return render(request, 'main/player_dashboard.html', {'title': 'Dashboard'})


@login_required()
def season_stats(request):
    return render(request, 'main/season_stats.html', {'title': 'Season Stats'})


@login_required()
def team_comparison(request):
    return render(request, 'main/team_comparison.html', {'title': 'Team Comparison'})
