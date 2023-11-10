from django.contrib import admin
from .models import AccountUser, group, group_member

# Register your models here.
admin.site.register(AccountUser)
admin.site.register(group)
admin.site.register(group_member)