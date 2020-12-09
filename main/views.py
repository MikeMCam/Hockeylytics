from django.shortcuts import render, redirect, get_object_or_404
from .models import Team, Match, PlayerList, Dummy, Stats
from users.models import Profile
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import TeamCreateForm
from django.core.exceptions import ObjectDoesNotExist, ValidationError, MultipleObjectsReturned
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
# TODO: Make it so coaches cannot enter in players with the same first + last name combination as 1 they already have
# TODO: When a coach deletes a team, delete the dummies on that team
@login_required()
def coach_dashboard(request):
    roster = None
    team = None
    if request.method == 'GET':
        if request.GET.get('teamDropdown'):
            try:
                team = Team.objects.get(coach=request.user, name=request.GET['teamDropdown'])
                roster = PlayerList.objects.filter(team=team)

            except ObjectDoesNotExist:
                pass

    # Delete team button
    if request.method == 'POST' and request.POST.get('deleteTeamSubmit') is not None:
        while True:
            if request.POST['deleteTeam'] == '---':
                messages.error(request, 'Please select a team to delete')
                break

            try:
                team = Team.objects.get(coach=request.user, name=request.POST['deleteTeam'])

                dummy_list = PlayerList.objects.filter(team=team, isDummy=True)
                print(dummy_list)
                for dummy in dummy_list:
                    dum = dummy.dummy
                    dum.delete()
                team.delete()
                messages.success(request, 'Team has been deleted')
                break
            except ObjectDoesNotExist:
                messages.error(request, 'Team deletion error')
                break

    # Only triggers when the 'create team' button is selected
    if request.method == 'POST' and request.POST.get('teamSubmit') is not None:

        while True:
            # Error messages
            if request.POST['nameField'] == '':
                messages.error(request, 'Please enter a name')
                break

            elif request.POST['countryField'] == '':
                messages.error(request, 'Please enter a country')
                break

            elif request.POST['stateField'] == '':
                messages.error(request, 'Please enter a state')
                break

            elif request.POST['cityField'] == '':
                messages.error(request, 'Please enter a city')
                break

            elif Team.objects.filter(coach=request.user, name=request.POST['nameField']).exists():
                messages.error(request, 'Team with this name already exists')
                break

            try:
                team = Team.objects.create(coach=request.user)
                team.name = request.POST['nameField']
                team.country = request.POST['countryField']
                team.state = request.POST['stateField']
                team.city = request.POST['cityField']
                team.save()
                messages.success(request, 'Team has been created')
                break
            except ObjectDoesNotExist:
                messages.error(request, 'data entry error')
                break

    # Only triggers when the 'create player' button is selected
    if request.method == 'POST' and request.POST.get('playerSubmit') is not None:
        while True:
            # Error messages
            if request.POST['playerTeam'] == '---':
                messages.error(request, 'Please select a team')
                break

            elif request.POST['playerFirstName'] == '':
                messages.error(request, 'Please enter a first name')
                break

            elif request.POST['playerLastName'] == '':
                messages.error(request, 'Please enter a last name')
                break

            try:
                dummy = Dummy.objects.create(createdBy=request.user)
                dummy.firstName = request.POST['playerFirstName']
                dummy.lastName = request.POST['playerLastName']
                dummy.save()
                dummy.refresh_from_db()
                add_dummy_to_team = PlayerList()
                add_dummy_to_team.dummy = Dummy.objects.get(firstName=request.POST['playerFirstName'],
                                                            lastName=request.POST['playerLastName'],
                                                            createdBy=request.user)

                add_dummy_to_team.isDummy = True
                add_dummy_to_team.player = None
                team = Team.objects.get(name=request.POST['playerTeam'], coach=request.user)
                add_dummy_to_team.team = team
                add_dummy_to_team.save()
                roster = PlayerList.objects.filter(team=team)
                messages.success(request, 'Player has been created')
                break
            except (ObjectDoesNotExist, MultipleObjectsReturned):
                messages.error(request, 'data entry error')
                break

    try:
        team_list = Team.objects.filter(coach=request.user)
    except ObjectDoesNotExist:
        team_list = None
    
    context = {
        'title': 'Dashboard',
        'team_list': team_list,
        'roster': roster,
        'team': team,
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
        team_list = Team.objects.filter(coach=user)
    except ObjectDoesNotExist:
        team_list = None

    context = {
        'title': 'Invite Players',
        'team_list': team_list,
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
            messages.success(request, f'Match has been created')
            return redirect(coach_dashboard)
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


# TODO: Fix high, except divide by zero error
# Stats -> user
@login_required()
def season_stats(request):
    user = request.user
    try:
        statList = Stats.objects.filter(player=user)
    except ObjectDoesNotExist:
        pass
    userGoals = 0
    userPoints = 0
    userFow= 0
    userFol = 0
    userPpg = 0
    userShg = 0
    userAssists = 0
    userFoPercent = 0
    userShootingPercent = 0
    userToi = 0
    userSog = 0
    userPim = 0

    for stat in statList:
        userGoals += stat.goals
        userPoints += stat.points
        userFow += stat.fow
        userFol += stat.fol
        userPpg += stat.ppg
        userShg += stat.shg
        userAssists += stat.assists
        userFoPercent += stat.foPercent
        userShootingPercent += stat.shootingPercent
        userToi += stat.toi
        userSog += stat.sog
        userPim += stat.pim

    def seasonHigh(x):
        max = 0
        for stat in statList:
            if x > max: max = x
        return max

    context = {
        'user_goals': userGoals,
        'user_points': userPoints,
        'user_fow': userFow,
        'user_fol': userFol,
        'user_ppg': userPpg,
        'user_shg': userShg,
        'user_assists': userAssists,
        'user_foPercent': userFoPercent,
        'user_shootingPercent': userShootingPercent,
        'user_toi': userToi,
        'user_sog': userSog,
        'user_pim': userPim,

        'ave_goals': round(userGoals / len(statList), 2),
        'ave_points': round(userPoints / len(statList), 2),
        'ave_fow': round(userFow / len(statList), 2),
        'ave_fol': round(userFol / len(statList), 2),
        'ave_ppg': round(userPpg / len(statList), 2),
        'ave_shg': round(userShg / len(statList), 2),
        'ave_assists': round(userAssists / len(statList), 2),
        'ave_foPercent': round(userFoPercent / len(statList), 2),
        'ave_shootingPercent': round(userShootingPercent / len(statList), 2),
        'ave_toi': round(userToi / len(statList), 2),
        'ave_sog': round(userSog / len(statList), 2),
        'ave_pim': round(userPim / len(statList), 2),

        'high_goals': seasonHigh(stat.goals),
        'high_points': seasonHigh(stat.points),
        'high_fow': seasonHigh(stat.fow),
        'high_fol': seasonHigh(stat.fol),
        'high_ppg': seasonHigh(stat.ppg),
        'high_shg': seasonHigh(stat.shg),
        'high_assists': seasonHigh(stat.assists),
        'high_foPercent': seasonHigh(stat.foPercent),
        'high_shootingPercent': seasonHigh(stat.shootingPercent),
        'high_toi': seasonHigh(stat.toi),
        'high_sog': seasonHigh(stat.sog),
        'high_pim': seasonHigh(stat.pim),
        'title': 'Season Stats',

    }
    return render(request, 'main/season_stats.html', context)


@login_required()
def team_comparison(request):
    return render(request, 'main/team_comparison.html', {'title': 'Team Comparison'})

