from django.contrib.auth.models import User
from django import forms

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class RegisterFormUser(forms.Form):
    firstname = forms.CharField(label='First name', max_length=100)
    surname = forms.CharField(label='Surname', max_length=100)

class RegisterFormMachine(forms.Form):
    machineName = forms.CharField(label='Machine name', max_length=100)
    machine_id = forms.CharField(label='Machine id', max_length=100)

class RegisterFormCard(forms.Form):
    cardNumber = forms.CharField(label='Card number', max_length=100)
