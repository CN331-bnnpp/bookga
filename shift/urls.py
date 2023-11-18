from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_shift, name='add'),
    path('', views.shifts_view, name='shifts_view'),
]