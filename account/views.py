from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .forms import LoginForm
from .models import User, group, group_member

# Create your views here.
@csrf_exempt
def login(request):
    if request.user.is_authenticated:
        user = request.user
        return render_login(request, user)
    
    if request.method == "GET":
        loginForm = LoginForm()
        return render(request, "login.html")
    
    elif request.method == "POST":
        users_id = request.POST["users_id"]
        password = request.POST["password"]
        user = authenticate(request, username=users_id, password=password)
        
        if user is not None:
            login(request, user)
            return render_login(request, user)
        else:
            messages.error(request, "Invalid username and/or password.")
            return render(request, "login.html")
    
def render_login(request, user):
    context = {
       user: user,
    }
    
    return render(request, "home.html", context)
    
