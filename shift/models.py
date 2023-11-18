from django.db import models
from account.models import group, AccountUser

# Create your models here.
class Shift(models.Model):
    Shift_id = models.AutoField(primary_key=True)
    group_name = models.ForeignKey(group, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    num_hours = models.IntegerField()
    num_people = models.IntegerField()
    
class ShiftUser(models.Model):
    shift_id = models.ForeignKey(Shift, on_delete=models.CASCADE)
    user_id = models.ForeignKey(AccountUser, on_delete=models.CASCADE)