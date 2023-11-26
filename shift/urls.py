from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_shift, name='add'),
    path('schedule/', views.shift_schedule, name='schedule'),
    path('book/', views.lookup_shift, name='book'),
]