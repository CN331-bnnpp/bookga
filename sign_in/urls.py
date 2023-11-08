from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('login/', views.SignInViaUsername, name='sign_in'),
    path('ok/', views.SignInTest, name='sign_in_test'),
    path('logout/', views.UserLogout, name='logout'),
]
