from django.contrib import admin
from .models import User, group, group_member

# Register your models here.
admin.site.register(User)
admin.site.register(group)
admin.site.register(group_member)