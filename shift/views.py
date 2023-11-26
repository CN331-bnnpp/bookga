import datetime
from django.shortcuts import render
from django.contrib import messages
from .forms import ShiftForm 
from .models import Shift, ShiftUser
from account.models import group, group_member

# Create your views here.
def add_shift(request):
    form = ShiftForm(request.POST)
    
    table = Shift.objects.all()    
    context = {
        'form': form,
        'table': table,
        'fields': ['Start Time', 'End Time', 'Number of People'],
    }
    
    if request.method == "POST":
        if form.is_valid():
            form.instance.group_name = group.objects.get(username=request.user)
            form.save()
            
            return render(request, "shift/add.html", context)
        
    return render(request, "shift/add.html", context)

def lookup_shift(request):
    table = Shift.objects.all()
    if request.user.is_staff:
        gn = group.objects.get(username=request.user).group_name
        table = Shift.objects.filter(group_name=gn)
    else:
        gn = group_member.objects.get(username=request.user).group_name
        table = Shift.objects.filter(group_name=gn)
    if request.method == "POST":
        return book_shift(request)
    
    count = {}
    for id in table.values_list('Shift_id', flat=True):
        count[id] = ShiftUser.objects.filter(shift_id=id).count()

    context = {
        'table': table,
        'fields': ['Start Time', 'End Time', 'Number of People', 'Book'],
        'count': count,
    }
    return render(request, "shift/book.html", context)

def shift_schedule(request):
    table = Shift.objects.all()
    if request.user.is_staff:
        gn = group.objects.get(username=request.user).group_name
        table = Shift.objects.filter(group_name=gn)
        book = ShiftUser.objects.filter(shift_id__in=table)
        
    else:
        gn = group_member.objects.get(username=request.user).group_name
        table = Shift.objects.filter(group_name=gn)
        book = ShiftUser.objects.filter(shift_id__in=table)

    context = {
        'table': generate_schedule(table, book),
        'times': ['12:00am', '1:00am', '2:00am', '3:00am', '4:00am', '5:00am',
                  '6:00am', '7:00am', '8:00am', '9:00am', '10:00am', '11:00am',
                  '12:00pm', '1:00pm', '2:00pm', '3:00pm', '4:00pm', '5:00pm',
                  '6:00pm', '7:00pm', '8:00pm', '9:00pm', '10:00pm', '11:00pm'],
        'user': request.user,
    }
    return render(request, "shift/schedule.html", context)

def generate_schedule(table, book):
    # Define the days of the week
    days_of_week = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

    # Initialize an empty schedule
    schedule = {}

    # Generate an empty schedule for each day of the week
    for day in days_of_week:
        daily_schedule = [''] * 24  # Placeholder for 6 activities
        schedule[day] = daily_schedule

    # Fill in the schedule with the activities
    for activity in table:
        start_time = activity.start_time
        num_hours = activity.num_hours

        # Find the day of the week
        tz = datetime.timezone(datetime.timedelta(hours=7))
        day = start_time.astimezone(tz).strftime('%a')

        # Find the index of the activity
        index = (start_time.hour + 7)%24

        # Fill in the activity
        schedule[day][index] = book.filter(shift_id=activity)

        # Fill in the activity for the next num_hours
        for i in range(1, num_hours):
            schedule[day][index + i] = book.filter(shift_id=activity)

    return schedule

def book_shift(request):
    if request.method == "POST":
        id = request.POST.get('id')
        shift = Shift.objects.get(pk=id)
        book = ShiftUser(shift_id=shift, user_id=request.user)
        if (shift.num_people > len(ShiftUser.objects.filter(shift_id=shift)) and
            not ShiftUser.objects.filter(shift_id=shift).filter(user_id=request.user).exists()):
            book.save()
        elif ShiftUser.objects.filter(shift_id=shift).filter(user_id=request.user).exists():
            messages.error(request, "You have already booked this shift")
        else:
            messages.error(request, "Shift is full")
    request.method = "GET"
    return lookup_shift(request)