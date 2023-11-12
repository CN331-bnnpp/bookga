from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('gate/', views.gate_view, name='gate'),
    path('imin/', views.imin, name='I am in'),
]
