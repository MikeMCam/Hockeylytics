from django.db import models
from django.contrib.auth.models import User
import uuid


class Team(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    coach = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)

    def __str__(self):
        return self.name


# Team roster
class PlayerList(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    join_date = models.DateTimeField()
    leave_date = models.DateTimeField(blank=True)

    def __str__(self):
        return f'{self.team} | {self.player}'


class Match(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateTimeField()
    homeTeam = models.ForeignKey(Team, null=True, related_name='home_team', on_delete=models.CASCADE)
    awayTeam = models.ForeignKey(Team, null=True, related_name='away_team', on_delete=models.CASCADE)
    homeGoals = models.IntegerField(default=0)
    homePoints = models.IntegerField(default=0)
    awayGoals = models.IntegerField(default=0)
    awayPoints = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.homeTeam} vs. {self.awayTeam}'


class Stats(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    player = models.ForeignKey(User, on_delete=models.CASCADE)

    FORWARD = 'FWD'
    DEFENSE = 'DEF'
    CENTER = 'CNT'
    GOALIE = 'GOL'
    POSITION_CHOICES = [
        (FORWARD, 'Forward'),
        (DEFENSE, 'Defense'),
        (CENTER, 'Center'),
        (GOALIE, 'Goalie'),
    ]
    position = models.CharField(
        max_length=3,
        choices=POSITION_CHOICES,
        default=FORWARD,
    )

    goals = models.IntegerField(blank=True, null=True)
    points = models.IntegerField(blank=True, null=True)
    fow = models.IntegerField(blank=True, null=True)
    fol = models.IntegerField(blank=True, null=True)
    ppg = models.IntegerField(blank=True, null=True)
    shg = models.IntegerField(blank=True, null=True)
    assists = models.IntegerField(blank=True, null=True)
    foPercent = models.FloatField(blank=True, null=True)
    shootingPercent = models.FloatField(blank=True, null=True)
    toi = models.IntegerField(blank=True, null=True)
    sog = models.IntegerField(blank=True, null=True)
    pim = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f'{self.match} | {self.player}'
