from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .forms import SignUpForm
from .models import User, group, group_member

# Create your views here.
def index(request):
    return render(request, "account/user.html")
@csrf_exempt
def login(request):
    if request.user.is_authenticated:
        user = request.user
        return render_login(request, user)
    
    if request.method == "GET":
        context = {
            "user_type": request.GET["user"],
        }
        print(context)
        return render(request, "account/login.html", context)
    
    elif request.method == "POST":
        users_id = request.POST["users_id"]
        password = request.POST["password"]
        user = authenticate(request, username=users_id, password=password)
        
        if user is not None:
            login(request, user)
            return render_login(request, user)
        else:
            messages.error(request, "Invalid username and/or password.")
            return render(request, "account/login.html")
    return render(request, "account/login.html")

def render_login(request, user):
    context = {
       user: user,
      # add
    }
    
    return render(request, "home/home.html", context)
    
def signup(request):
    if request.method == "GET":
        signupForm = SignUpForm()
        return render(request, "account/signup.html")
    
    elif request.method == "POST":
        signupForm = SignUpForm(request.POST)
        
        if signupForm.is_valid():
            signupForm.save()
            messages.success(request, "Account created successfully.")
            return redirect("home")
        else:
            messages.error(request, "Invalid form.")
            return render(request, "account/signup.html")