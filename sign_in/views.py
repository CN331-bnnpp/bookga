from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError
from .forms import SignInViaUsernameForm ,createUserForm


def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            #redirect to staff page
            #in this step render test page
            return render(request, 'sign_in\sign-in-test.html',{'user': request.user,'user.username': request.user.username})
            

        else:
            #redirect to user page
            #in this step render test page
            return render(request, 'sign_in\sign-in-test.html',{'user': request.user,'user.username': request.user.username})

    if request.method == 'GET':
        #in case method is GET, which should not happen. render login form
        render(request,'gate/gate.html',{'user': request.user,'LoginForm': SignInViaUsernameForm(),'SignupForm': createUserForm()})

    elif request.method == 'POST':
        #redirect to a form
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
                #redirect to staff page
                #in this step render test page
                return render(request, 'sign_in\sign-in-test.html',{'user': request.user,'user.username': request.user.username})
            else:
                #redirect to user page
                #in this step render test page
                return render(request, 'sign_in\sign-in-test.html',{'user': request.user,'user.username': request.user.username})

    #in case everything else, which should not happen. render login form
    return render(request,'gate/gate.html',{'user': request.user,'LoginForm': SignInViaUsernameForm(),'SignupForm': createUserForm()})

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('/login')



def gate_view(request):
    return render(request,'gate/gate.html',{'user': request.user,'LoginForm': SignInViaUsernameForm(),'SignupForm': createUserForm()})