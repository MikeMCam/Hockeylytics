from django import forms
from .models import Match


class TeamCreateForm(forms.ModelForm):

    class Meta:
        model = Match
        fields = ['date', 'homeTeam', 'awayTeam', 'homeGoals', 'homePoints', 'awayGoals', 'awayPoints']
        widgets = {
            'date': forms.TextInput(attrs={'placeholder': 'MM/DD/YYYY'})
        }
