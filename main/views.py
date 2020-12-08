from django.shortcuts import render, redirect, get_object_or_404
from .models import Team, Match, PlayerList, Dummy, Stats
from users.models import Profile
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import TeamCreateForm
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.http import JsonResponse
from django.http import HttpResponse


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


# TODO: IMPORTANT!!!!! Make sure to not allow coaches to make teams or players
#  with the same name as one they already have
# TODO: Add ajax to this so it isn't so awkward

# For this to work:
# 1. When a new player is created, it should be made as a dummy first, taking first name, last name,
#    createdBy = request.user
# 2. When the stats is created, all playerList entries on that team should be shown for the user to select. If a dummy
#    is selected, the stats should also do: isDummy = True, Dummy = PlayerList.Dummy. If a user is selected, isDummy =
#    False and Dummy = None
@login_required()
def invite_players(request):

    roster = None
    team = None
    # fetches the players from the currently selected team
    if request.method == 'GET':
        if request.GET.get('teamDropdown'):
            try:
                team = Team.objects.get(coach=request.user, name=request.GET['teamDropdown'])
                roster = PlayerList.objects.filter(team=team, isDummy=True)

            except ObjectDoesNotExist:
                pass

    # Submits the final form and checks for errors
    if request.method == 'POST':
        while True:
            # Error messages
            if request.POST['finalTeam'] == 'None':
                messages.error(request, 'Please select a team')
                break

            elif request.POST['playerSelect'] == '---':
                messages.error(request, 'Please select a player')
                break

            elif len(request.POST['playerID']) != 36:
                messages.error(request, 'Please enter a valid player ID')
                break

            elif Profile.objects.get(unique_id=request.POST['playerID']).user_type == 'CH':
                messages.error(request, 'User with this ID is not a player')
                break

            try:
                user = Profile.objects.get(unique_id=request.POST['playerID']).user
                player_name = request.POST['playerSelect'].split(" ", 2)
                print(f'{player_name[0]} {player_name[1]}')
                dummy = Dummy.objects.get(firstName=player_name[0], lastName=player_name[1], createdBy=request.user)
                team = Team.objects.get(coach=request.user, name=request.POST['finalTeam'])
                player = PlayerList.objects.get(team=team, isDummy=True, dummy=dummy)

                player.isDummy = False
                player.dummy = None
                player.player = user

                stats = Stats.objects.filter(isDummy=True, dummy=dummy)

                for stat in stats:
                    stat.isDummy = False
                    stat.dummy = None
                    stat.player = user
                    stat.save()
                player.save()
                dummy.delete()
                messages.success(request, 'Player now has access to their stats from {team.name}')
                break

            except (ObjectDoesNotExist, ValidationError):
                messages.error(request, 'an error occurred')
                break

    # Fetches the teams owned by the logged in user
    user = request.user
    try:
        teamList = Team.objects.filter(coach=user)
    except ObjectDoesNotExist:
        teamList = None

    context = {
        'title': 'Invite Players',
        'team_list': teamList,
        'roster': roster,
        'team': team,
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

