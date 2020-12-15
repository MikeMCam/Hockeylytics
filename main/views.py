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
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
import pandas as pd
import datetime


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
    stat_1 =None
    graph = None
    graph_2 = None
    stats_list = {}

    # -------------------------------------------- PLAYER BREAKDOWN ----------------------------------------------------
    if request.POST.get('player-breakdown-submit') is not None:
        print(request.POST)
        while True:
            try:
                if request.POST.get('player-breakdown-team') == 'None':
                    messages.error(request, 'Please select a team')
                    break
                if request.POST.get('player-breakdown-roster') == '---':
                    messages.error(request, 'Please select a player')
                    break
                if request.POST.get('player-breakdown-stat') == '---':
                    messages.error(request, 'Please select a stat')
                    break
                messages.success(request, 'We are in Player Breakdown')
                break
            except ObjectDoesNotExist:
                messages.error(request, 'Player Breakdown ODNE Error')
                break
    # -------------------------------------------- CHOOSE A STAT -------------------------------------------------------
    if request.GET.get('stat-select') is not None:
        stat_1 = request.GET.get('stat-select')
        try:
            if request.GET.get('stat-select') == 'Goals':
                team = Team.objects.get(coach=request.user, name=request.GET['teamChoice'])
                roster = PlayerList.objects.filter(team=team)
                player_list = PlayerList.objects.filter(team=team)
                stats_list = {}
                total_goals = 0
                for player in player_list:
                    if player.isDummy:
                        stats = Stats.objects.filter(dummy=player.dummy)
                        for stat in stats:
                            total_goals += stat.goals
                        stats_list.update({f'{player.dummy.firstName} {player.dummy.lastName}': total_goals})
                        total_goals = 0

                    else:
                        stats = Stats.objects.filter(player=player.player)
                        for stat in stats:
                            total_goals += stat.goals
                        stats_list.update({f'{player.player.first_name} {player.player.last_name}': total_goals})
                        total_goals = 0
                df = pd.DataFrame(list(stats_list.items()), columns=['Team Players', 'Goals'])
                fig = px.scatter(df, x="Team Players", y="Goals", template='plotly_dark')
                graph = fig.to_html(full_html=False, default_height=500, default_width=700)

            if request.GET.get('stat-select') == 'Assists':
                team = Team.objects.get(coach=request.user, name=request.GET['teamChoice'])
                roster = PlayerList.objects.filter(team=team)
                player_list = PlayerList.objects.filter(team=team)
                stats_list = {}
                total_assists = 0
                for player in player_list:
                    if player.isDummy:
                        stats = Stats.objects.filter(dummy=player.dummy)
                        for stat in stats:
                            total_assists += stat.assists
                        stats_list.update({f'{player.dummy.firstName} {player.dummy.lastName}': total_assists})
                        total_assists = 0

                    else:
                        stats = Stats.objects.filter(player=player.player)
                        for stat in stats:
                            total_assists += stat.assists
                        stats_list.update({f'{player.player.first_name} {player.player.last_name}': total_assists})
                        total_assists = 0
                df = pd.DataFrame(list(stats_list.items()), columns=['Team Players', 'Assists'])
                fig = px.scatter(df, x="Team Players", y="Assists", template='plotly_dark')
                graph = fig.to_html(full_html=False, default_height=500, default_width=700)

            if request.GET.get('stat-select') == 'Points':
                team = Team.objects.get(coach=request.user, name=request.GET['teamChoice'])
                roster = PlayerList.objects.filter(team=team)
                player_list = PlayerList.objects.filter(team=team)
                stats_list = {}
                total_points = 0
                for player in player_list:
                    if player.isDummy:
                        stats = Stats.objects.filter(dummy=player.dummy)
                        for stat in stats:
                            total_points += stat.points
                        stats_list.update({f'{player.dummy.firstName} {player.dummy.lastName}': total_points})
                        total_points = 0

                    else:
                        stats = Stats.objects.filter(player=player.player)
                        for stat in stats:
                            total_points += stat.points
                        stats_list.update({f'{player.player.first_name} {player.player.last_name}': total_points})
                        total_points = 0
                df = pd.DataFrame(list(stats_list.items()), columns=['Team Players', 'Points'])
                fig = px.scatter(df, x="Team Players", y="Points", template='plotly_dark')
                graph = fig.to_html(full_html=False, default_height=500, default_width=700)

            if request.GET.get('stat-select') == 'ppg':
                team = Team.objects.get(coach=request.user, name=request.GET['teamChoice'])
                roster = PlayerList.objects.filter(team=team)
                player_list = PlayerList.objects.filter(team=team)
                stats_list = {}
                total_ppg = 0
                for player in player_list:
                    if player.isDummy:
                        stats = Stats.objects.filter(dummy=player.dummy)
                        for stat in stats:
                            total_ppg += stat.ppg
                        stats_list.update({f'{player.dummy.firstName} {player.dummy.lastName}': total_ppg})
                        total_ppg = 0

                    else:
                        stats = Stats.objects.filter(player=player.player)
                        for stat in stats:
                            total_ppg += stat.ppg
                        stats_list.update({f'{player.player.first_name} {player.player.last_name}': total_ppg})
                        total_ppg = 0
                df = pd.DataFrame(list(stats_list.items()), columns=['Team Players', 'Power Play Goals'])
                fig = px.scatter(df, x="Team Players", y="Power Play Goals", template='plotly_dark')
                graph = fig.to_html(full_html=False, default_height=500, default_width=700)

            if request.GET.get('stat-select') == 'ppp':
                team = Team.objects.get(coach=request.user, name=request.GET['teamChoice'])
                roster = PlayerList.objects.filter(team=team)
                player_list = PlayerList.objects.filter(team=team)
                stats_list = {}
                total_ppp = 0
                for player in player_list:
                    if player.isDummy:
                        stats = Stats.objects.filter(dummy=player.dummy)
                        for stat in stats:
                            total_ppp += stat.ppp
                        stats_list.update({f'{player.dummy.firstName} {player.dummy.lastName}': total_ppp})
                        total_ppp = 0

                    else:
                        stats = Stats.objects.filter(player=player.player)
                        for stat in stats:
                            total_ppp += stat.ppp
                        stats_list.update({f'{player.player.first_name} {player.player.last_name}': total_ppp})
                        total_ppp = 0
                df = pd.DataFrame(list(stats_list.items()), columns=['Team Players', 'Power Play Points'])
                fig = px.scatter(df, x="Team Players", y="Power Play Points", template='plotly_dark')
                graph = fig.to_html(full_html=False, default_height=500, default_width=700)

            if request.GET.get('stat-select') == 'toi':
                team = Team.objects.get(coach=request.user, name=request.GET['teamChoice'])
                roster = PlayerList.objects.filter(team=team)
                player_list = PlayerList.objects.filter(team=team)
                stats_list = {}
                total_toi = 0
                for player in player_list:
                    if player.isDummy:
                        stats = Stats.objects.filter(dummy=player.dummy)
                        for stat in stats:
                            total_toi += stat.toi
                        toi_as_time = str(datetime.timedelta(seconds=total_toi))
                        stats_list.update({f'{player.dummy.firstName} {player.dummy.lastName}': toi_as_time})
                        total_toi = 0

                    else:
                        stats = Stats.objects.filter(player=player.player)
                        for stat in stats:
                            total_toi += stat.toi
                        toi_as_time = str(datetime.timedelta(seconds=total_toi))
                        stats_list.update({f'{player.player.first_name} {player.player.last_name}': toi_as_time})
                        total_toi = 0

                df = pd.DataFrame(list(stats_list.items()), columns=['Team Players', 'TOI'])
                fig = px.scatter(df, x="Team Players", y="TOI", template='plotly_dark')
                graph = fig.to_html(full_html=False, default_height=500, default_width=700)

            if request.GET.get('stat-select') == 'fop':
                team = Team.objects.get(coach=request.user, name=request.GET['teamChoice'])
                roster = PlayerList.objects.filter(team=team)
                player_list = PlayerList.objects.filter(team=team)
                stats_list = {}
                total_fop = 0
                for player in player_list:
                    if player.isDummy:
                        stats = Stats.objects.filter(dummy=player.dummy)
                        for stat in stats:
                            total_fop += stat.foPercent
                        stats_list.update({f'{player.dummy.firstName} {player.dummy.lastName}': total_fop})
                        total_fop = 0

                    else:
                        stats = Stats.objects.filter(player=player.player)
                        for stat in stats:
                            total_fop += stat.foPercent
                        stats_list.update({f'{player.player.first_name} {player.player.last_name}': total_fop})
                        total_fop = 0
                df = pd.DataFrame(list(stats_list.items()), columns=['Team Players', 'Face-off Percentage'])
                fig = px.scatter(df, x="Team Players", y="Face-off Percentage", template='plotly_dark')
                graph = fig.to_html(full_html=False, default_height=500, default_width=700)

            if request.GET.get('stat-select') == 'shoop':
                team = Team.objects.get(coach=request.user, name=request.GET['teamChoice'])
                roster = PlayerList.objects.filter(team=team)
                player_list = PlayerList.objects.filter(team=team)
                stats_list = {}
                total_shoop = 0
                for player in player_list:
                    if player.isDummy:
                        stats = Stats.objects.filter(dummy=player.dummy)
                        for stat in stats:
                            total_shoop += stat.shootingPercent
                        stats_list.update({f'{player.dummy.firstName} {player.dummy.lastName}': total_shoop})
                        total_shoop = 0

                    else:
                        stats = Stats.objects.filter(player=player.player)
                        for stat in stats:
                            total_shoop += stat.shootingPercent
                        stats_list.update({f'{player.player.first_name} {player.player.last_name}': total_shoop})
                        total_shoop = 0
                df = pd.DataFrame(list(stats_list.items()), columns=['Team Players', 'Shooting Percentage'])
                fig = px.scatter(df, x="Team Players", y="Shooting Percentage", template='plotly_dark')
                graph = fig.to_html(full_html=False, default_height=500, default_width=700)

        except ObjectDoesNotExist:
            messages.error(request, 'error')
            pass
    # ------------------------------------------ FIND TEAMS ------------------------------------------------------------
    if request.method == 'GET':
        if request.GET.get('teamDropdown'):
            try:
                # Get what team the user selected in the dropdown
                team = Team.objects.get(coach=request.user, name=request.GET['teamDropdown'])
                # Lookup every player on that team
                roster = PlayerList.objects.filter(team=team)
                player_list = PlayerList.objects.filter(team=team)

            except ObjectDoesNotExist:
                pass

    # ------------------------------------------ DELETE TEAM -----------------------------------------------------------
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

    # ------------------------------------------ DELETE PLAYER ---------------------------------------------------------
    if request.method == 'POST' and request.POST.get('removePlayerSubmit') is not None:
        while True:
            if request.POST['deletePlayerPlayer'] == '---':
                messages.error(request, 'Please select a player')
                break

            try:
                word = request.POST['deletePlayerPlayer']
                if 'unlinked' not in word:

                    first_name = word.split(' ', 1)[0]
                    last_name = word.split(' ', 1)[1]
                    pp = User.objects.get(first_name=first_name, last_name=last_name)
                    pp_list = PlayerList.objects.get(player=pp, team=request.POST['deletePlayerTeam'])
                    pp_list.delete()
                else:
                    print('unlinked found')
                    pp = Dummy.objects.get(firstName=word.split(' ')[0], lastName=word.split(' ')[1])
                    pp.delete()
                messages.success(request, "player has been removed")
                break
            except ObjectDoesNotExist:
                messages.error(request, 'Player removal error')
                break

    # ------------------------------------------ CREATE TEAM  ----------------------------------------------------------
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

    # ------------------------------------------ CREATE PLAYER ---------------------------------------------------------
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

            # scuffed way of checking for duplicate names
            full_name = request.POST['playerFirstName'] + " " + request.POST['playerLastName']
            print(f'full_name = {full_name}')
            should_break = False
            playerList = PlayerList.objects.filter(team=Team.objects.get(coach=request.user,
                                                                         name=request.GET['teamDropdown']))
            for player in playerList:
                if player.isDummy:
                    dummy_name = player.dummy.firstName + " " + player.dummy.lastName
                    if dummy_name == full_name:
                        print(f'dummy_name = {dummy_name}')
                        should_break = True
                else:
                    player_name = player.player.first_name + " " + player.player.last_name
                    if player_name == full_name:
                        print(f'player_name = {player_name}')
                        should_break = True
            if should_break:
                messages.error(request, 'please enter a unique player name')
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

    # ----------------------------------- CONTEXT / END ----------------------------------------------------------------
    try:
        team_list = Team.objects.filter(coach=request.user)
    except ObjectDoesNotExist:
        team_list = None

    context = {
        'title': 'Dashboard',
        'team_list': team_list,
        'roster': roster,
        'team': team,
        'stat_1': stat_1,
        'graph': graph,
        'graph-2': graph_2,
    }
    return render(request, 'main/coach_dashboard.html', context)


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
            form.instance.createdBy = request.user
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
    match = None
    if request.method == 'GET':
        if request.GET.get('teamListDropDown'):
            try:
                match = Team.objects.filter(coach=request.user)
            except ObjectDoesNotExist:
                pass

    context = {
        'match': match,
        'title': 'Games'}

    return render(request, 'main/game_list.html', context)


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
    aveGoals = 0
    highGoals = 0

    userPoints = 0
    avePoints = 0
    highPoints = 0

    userFow = 0
    aveFow = 0
    highFow = 0

    userFol = 0
    aveFol = 0
    highFol = 0

    userPpg = 0
    avePpg = 0
    highPpg = 0

    userShg = 0
    aveShg = 0
    highShg = 0

    userAssists = 0
    aveAssists = 0
    highAssists = 0

    userFoPercent = 0
    aveFoPercent = 0
    highFoPercent = 0

    userShootingPercent = 0
    aveShootingPercent = 0
    highShootingPercent = 0

    userToi = 0
    aveToi = 0
    highToi = 0

    userSog = 0
    aveSog = 0
    highSog = 0

    userPim = 0
    avePim = 0
    highPim = 0

    if len(statList) != 0:
        for stat in statList:
            userGoals += stat.goals
            aveGoals = (aveGoals + stat.goals) / len(statList)
            if stat.goals > highGoals:
                highGoals = stat.goals

            userPoints += stat.points
            avePoints = (avePoints + stat.points) / len(statList)
            if stat.points > highPoints:
                highPoints = stat.points

            userFow += stat.fow
            aveFow = (aveFow + stat.fow) / len(statList)
            if stat.fow > highFow:
                highFow = stat.fow

            userFol += stat.fol
            aveFol = (aveFol + stat.fol) / len(statList)
            if stat.fol > highFol:
                highFol = stat.fol

            userPpg += stat.ppg
            avePpg = (avePpg + stat.ppg) / len(statList)
            if stat.ppg > highPpg:
                highPpg = stat.ppg

            userShg += stat.shg
            aveShg = (aveShg + stat.shg) / len(statList)
            if stat.shg > highShg:
                highShg = stat.shg

            userAssists += stat.assists
            aveAssists = (aveAssists + stat.assists) / len(statList)
            if stat.assists > highAssists:
                highAssists = stat.assists

            userFoPercent += stat.foPercent
            aveFoPercent = (aveFoPercent + stat.foPercent) / len(statList)
            if stat.foPercent > highFoPercent:
                highFoPercent = stat.foPercent

            userShootingPercent += stat.shootingPercent
            aveShootingPercent = (aveShootingPercent + stat.shootingPercent) / len(statList)
            if stat.shootingPercent > highShootingPercent:
                highShootingPercent = stat.shootingPercent

            userToi += stat.toi
            aveToi = (aveToi + stat.toi) / len(statList)
            if stat.toi > highToi:
                highToi = stat.toi

            userSog += stat.sog
            aveSog = (aveSog + stat.sog) / len(statList)
            if stat.sog > highSog:
                highSog = stat.sog

            userPim += stat.pim
            avePim = (avePim + stat.pim) / len(statList)
            if stat.pim > highPim:
                highPim = stat.pim

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

        'ave_goals': round(aveGoals, 2),
        'ave_points': round(avePoints, 2),
        'ave_fow': round(aveFow, 2),
        'ave_fol': round(aveFol, 2),
        'ave_ppg': round(avePpg, 2),
        'ave_shg': round(aveShg, 2),
        'ave_assists': round(aveAssists, 2),
        'ave_foPercent': round(aveFoPercent, 2),
        'ave_shootingPercent': round(aveShootingPercent, 2),
        'ave_toi': round(aveToi, 2),
        'ave_sog': round(aveSog, 2),
        'ave_pim': round(avePim, 2),

        'high_goals': highGoals,
        'high_points': highPoints,
        'high_fow': highFow,
        'high_fol': highFol,
        'high_ppg': highPpg,
        'high_shg': highShg,
        'high_assists': highAssists,
        'high_foPercent': highFoPercent,
        'high_shootingPercent': highShootingPercent,
        'high_toi': highToi,
        'high_sog': highSog,
        'high_pim': highPim,
        'title': 'Season Stats',

    }

    return render(request, 'main/season_stats.html', context)


@login_required()
def team_comparison(request):
    return render(request, 'main/team_comparison.html', {'title': 'Team Comparison'})
