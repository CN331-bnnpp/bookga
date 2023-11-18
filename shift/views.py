from django.shortcuts import render ,redirect
from .forms import ShiftForm ,BookingForm
from .models import Shift, ShiftUser
from account.models import group, group_member

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
        
    print(table.values_list('start_time', flat=True)[0])
    return render(request, "shift/add.html", context)




def shifts_view(request):
    user_group = group_member.objects.filter(username=request.user).first()

    if user_group:
        shifts = Shift.objects.filter(group_name=user_group.group_name)

        return render(request, 'shift/shifts.html', {'shifts': shifts})
    else:
        print('error no group')
        return render(request, 'shift/shifts.html')
