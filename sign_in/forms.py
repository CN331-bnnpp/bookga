from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

class SignInViaUsernameForm(forms.Form):
    username = forms.CharField(label="username",max_length=25)
    password = forms.CharField(label=('Password'), max_length=25, widget=forms.PasswordInput)



        
    