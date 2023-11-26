from django.shortcuts import render
from shift.models import ShiftUser
from django_pandas.io import read_frame

# Create your views here.
def report(request):
    shift_users = ShiftUser.objects.all()
    df = read_frame(shift_users)
    df['shift_id'] = df['shift_id'].apply(lambda x: x[-2])
    # get day from start_time 
    day = []
    month = []
    year = []
    for i in ShiftUser.objects.values('shift_id__start_time'):
        day.append(i['shift_id__start_time'].strftime("%A")[:3])
        month.append(i['shift_id__start_time'].strftime("%B")[:3])
        year.append(i['shift_id__start_time'].strftime("%Y"))
    df['day'] = day
    df['month'] = month
    df['year'] = year
    context = {
        'countDay': countDay(df),
        'countMonth': countMonth(df),
    }  
    
    return render(request, 'report/report.html', context)

def countDay(df):
    df = df.groupby(['day']).count()
    df = df.reset_index()
    day = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    data = {}
    for i in day:
        data[i] = df[df['day'] == i]['id'].tolist()
        if data[i]:
            data[i] = data[i][0]
        else:
            data[i] = 0
    return data

def countMonth(df):
    df = df.groupby(['month']).count()
    df = df.reset_index()
    month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    data = {}
    for i in month:
        data[i] = df[df['month'] == i]['id'].tolist()
        if data[i]:
            data[i] = data[i][0]
        else:
            data[i] = 0
    return data