from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


# TODO: add user_type to users database
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    CHOICES = [('Coach', 'Coach'), ('Player', 'Player')]
    user_type = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = User
        fields = ['username', 'user_type', 'email', 'password1', 'password2']
