from django.contrib import admin
from .models import Shift, ShiftUser

# Register your models here.
class ShiftAdmin(admin.ModelAdmin):
    model = Shift
    list_display = ['Shift_id', 'group_name', 'start_time', 'num_hours', 'num_people']
    
class ShiftUserAdmin(admin.ModelAdmin):
    model = ShiftUser
    list_display = ['shift_id', 'user_id']
    
admin.site.register(Shift, ShiftAdmin)
admin.site.register(ShiftUser, ShiftUserAdmin)