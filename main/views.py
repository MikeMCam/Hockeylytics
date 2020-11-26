from django.shortcuts import render


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
def coach_dashboard(request):
    context = {
        'title': 'Dashboard',
    }
    return render(request, 'main/coach_dashboard.html', context)


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
