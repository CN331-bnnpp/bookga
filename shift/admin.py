from django.contrib import admin
from .models import Shift

# Register your models here.
class ShiftAdmin(admin.ModelAdmin):
    model = Shift
    list_display = ['Shift_id', 'group_name', 'start_time', 'num_hours', 'num_people']
    
admin.site.register(Shift, ShiftAdmin)