from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError
from .forms import SignInViaUsernameForm ,createUserForm
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def login_view(request):
    current_view = ''
    if request.user.is_authenticated:
        if request.user.is_staff:
            # redirect to staff page 
            # now render test page
            return render(request, 'sign_in/sign-in-test.html', {'user': request.user, 'username': request.user.username})
        else:
            # redirect to user page 
            # now render test page
            return render(request, 'sign_in/sign-in-test.html', {'user': request.user, 'username': request.user.username})

    if request.method == 'POST':
        sign_in_form = SignInViaUsernameForm(request.POST)
        if sign_in_form.is_valid():
            sign_in_form.login(request)
            # redirect to user page 
            # now render test page
            return render(request, 'sign_in/sign-in-test.html', {'user': request.user, 'username': request.user.username})
        else:
            current_view = 'login'
    if request.method == 'GET':
        sign_in_form = SignInViaUsernameForm(request.POST)
    # if the request is a GET or the form is not valid, render the login form
    return render(request, 'gate/gate.html', {'user': request.user, 'LoginForm': sign_in_form, 'SignupForm': createUserForm(), 'current_view': current_view})


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('/login')



def gate_view(request):
    return render(request,'gate/gate.html',{'user': request.user,'LoginForm': SignInViaUsernameForm(),'SignupForm': createUserForm()})