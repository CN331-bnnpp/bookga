from django.contrib import admin
from .models import  group, group_member,AccountUser


# Register your models here.
admin.site.register(AccountUser)
admin.site.register(group)
admin.site.register(group_member)