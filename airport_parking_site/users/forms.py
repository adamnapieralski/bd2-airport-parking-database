from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from parking_app.models import Klient


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username',
            'password1',
            'password2'
        ]


class KlientForm(forms.ModelForm):
    nr_tel = forms.IntegerField()

    class Meta:
        model = Klient
        fields = [
            'imie',
            'nazwisko',
            'nr_tel'
        ]
