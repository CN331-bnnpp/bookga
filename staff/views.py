from django.shortcuts import render

# Create your views here.
def staff_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            pass
            #render staff_view
        else:
            pass
            #redirect to user_view
    else:
        #redirect to login_view
        pass