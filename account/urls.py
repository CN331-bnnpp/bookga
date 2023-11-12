from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_app, name='login'),
    path('signup/', views.signup, name='signup'),
    path('create/', views.create_member, name='create'),
]