from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import Utente


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Utente
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2', 'acceptance')


class SignupForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'type': 'password', 'name': 'password', 'placeholder': 'Password'}),
        label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'type': 'password', 'name': 'password', 'placeholder': 'Password'}),
        label='Conferma password')
    acceptance = forms.BooleanField(required=True)

    class Meta:
        model = Utente
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2', 'acceptance', 'newsletter')
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control", }),
            "last_name": forms.TextInput(attrs={"class": "form-control", }),
            "email": forms.EmailInput(attrs={"class": "form-control", }),
            "acceptance": forms.CheckboxInput(
                attrs={"class": "form-check-input", "type": "checkbox", "id": "acceptanceCheck"}),
            "newsletter": forms.CheckboxInput(
                attrs={"class": "form-check-input", "type": "checkbox", "id": "newsletterCheck"}),
        }


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = Utente
        fields = ('email', 'first_name', 'last_name', 'username',)
