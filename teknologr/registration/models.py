from django.db import models
from django import forms


class RegistrationForm(forms.Form):
    surname = forms.CharField(label='Efternamn', max_length=100)

