from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError
from .forms import SignInViaUsernameForm ,createUserForm
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt

def login_view(request):
    current_view = ''
    signup_form = createUserForm()
    login_form = SignInViaUsernameForm()

    if request.user.is_authenticated:
        if request.user.is_staff:
             # redirect to staff page ,now rendering test page
            return render(request, 'sign_in/sign-in-test.html', {'user': request.user, 'username': request.user.username})
        else:
            # redirect to user page ,now rendering test page
            return render(request, 'sign_in/sign-in-test.html', {'user': request.user, 'username': request.user.username})

    if request.method == 'POST':
        if 'signup' in request.POST:
            print('signup is clicked')
            signup_form = createUserForm(request.POST)
            if signup_form.is_valid():
                new_user = signup_form.createUser()
                if new_user:
                    login(request, new_user)
                    # redirect to staff page ,now rendering test page
                    return render(request, 'sign_in/sign-in-test.html', {'user': request.user, 'username': request.user.username})
            current_view = 'signup'

        elif 'login' in request.POST:
            print('signup is login')
            login_form = SignInViaUsernameForm(request.POST)
            if login_form.is_valid():
                login_form.login(request)
                 # redirect to user page ,now rendering test page
                return render(request, 'sign_in/sign-in-test.html', {'user': request.user, 'username': request.user.username})

            current_view = 'login'

    return render(request, 'gate/gate.html', {'user': request.user, 'LoginForm': login_form, 'SignupForm': signup_form, 'current_view': current_view})



def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('/login')



def gate_view(request):
    return render(request,'gate/gate.html',{'user': request.user,'LoginForm': SignInViaUsernameForm(),'SignupForm': createUserForm()})