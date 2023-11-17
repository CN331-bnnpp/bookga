from django.urls import path
from .views import *
from django.contrib import admin 
admin.autodiscover()

urlpatterns = [
    path('month/<int:month>/<int:year>/', MonthDetailView.as_view(), name='month_detail'),
    path('reservation/', Reservation.as_view(), name='reservations_reservation'),
    path('calendar/', calendar_view, name='reservations_calendar'),
    path('holidays/', get_holidays, name='reservations_holidays'),
]
