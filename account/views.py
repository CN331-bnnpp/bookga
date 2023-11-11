from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.models import User
from .models import group

# Create your views here.
def index(request):
    print(User.objects.count())
    return render(request, "account/types.html")

@csrf_exempt
def login_app(request):
    if request.user.is_authenticated:
        user = request.user
        return render_login(request, user)
    
    if request.method == "GET":
        context = {
            "user_type": request.GET["user"],
        }
        return render(request, "account/login.html", context)
    
    elif request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        
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
    if user.is_superuser:
        return render(request, "account/admin.html", context)
    elif user.is_staff:
        return render(request, "account/staff.html", context)
    
    return render(request, "account/user.html", context)
    
def signup(request):
    signupForm = UserCreationForm(request.POST)
    if request.method == "GET":
        return render(request, "account/signup.html", {"form": signupForm})
    
    elif request.method == "POST":
        if signupForm.is_valid():
            signupForm.instance.is_staff = True
            signupForm.save()
            username = signupForm.cleaned_data.get('username')
            password = signupForm.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            group_name = request.POST["group_name"]
            create = group.objects.create(username=user, group_name=group_name)
            create.save()
            messages.success(request, "Account created successfully.")
            return render_login(request, user)
        else:
            messages.error(request, "Invalid form.")
            return render(request, "account/signup.html", {"form": signupForm})