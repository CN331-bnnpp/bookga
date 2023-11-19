from django.shortcuts import render
from .forms import ShiftForm 
from .models import Shift
from account.models import group

# Create your views here.
def add_shift(request):
    form = ShiftForm(request.POST)
    
    table = Shift.objects.all()    
    context = {
        'form': form,
        'table': table,
        'fields': ['start_time', 'num_hours', 'num_people'],
    }
    
    if request.method == "POST":
        if form.is_valid():
            form.instance.group_name = group.objects.get(username=request.user)
            form.save()
            
            return render(request, "shift/add.html", context)
        
    return render(request, "shift/add.html", context)