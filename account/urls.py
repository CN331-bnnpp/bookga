from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_app, name='login'),
    path('logout/', views.logout_app, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('create/', views.create_member, name='create'),
    path('staff/', views.staff_view, name='staff_view'),
    path('user/', views.user_view, name='user_view'),
]