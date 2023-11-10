from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('login/', views.login_view, name='sign_in'),
    path('logout/', views.logout_view, name='logout'),
    path('gate/', views.gate_view, name='logout'),
]
