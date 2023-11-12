from django.contrib import admin
from .models import AccountUser, group, group_member

# Register your models here.
class AccountUserAdmin(admin.ModelAdmin):
    model = AccountUser
    list_display = ['username', 'email', 'is_staff', 'is_active', 'date_joined']
    
class groupAdmin(admin.ModelAdmin):
    model = group
    list_display = ['username', 'group_name']
    
class group_memberAdmin(admin.ModelAdmin):
    model = group_member
    list_display = ['username', 'group_name']

admin.site.register(AccountUser, AccountUserAdmin)
admin.site.register(group, groupAdmin)
admin.site.register(group_member, group_memberAdmin)
