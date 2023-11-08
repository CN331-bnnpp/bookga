from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError
from .forms import SignInViaUsernameForm


def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            pass
            #render staff page

        else:
            pass
            #render user page

    if request.method == 'GET':
        #in case method is GET, which should not happen. render login form
        return render(request, 'users/login.html', {'form': SignInViaUsernameForm()})

    elif request.method == 'POST':
        #render a form
        form = SignInViaUsernameForm(request.POST)
        #if the input is valid
        if form.is_valid():
            #get and clean the username and password input
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            #authenticate user using cleaned username and password
            user = authenticate(request, username=username, password=password)

            #in case that username and password no match
            if user is None:
                raise ValidationError("Invalid username or password!")

            #in case that user is not active
            if not user.is_active:
                raise ValidationError("This account is inactive.")

            #login with authenticated user
            login(request, user)

            if user.is_staff:
                pass
                #render staff page
            else:
                pass
                #render user page

    #in case everything else, which should not happen. render login form
    return render(request, 'users/login.html', {'form': SignInViaUsernameForm()})

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('login_view')



