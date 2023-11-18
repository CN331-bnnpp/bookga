from django.db import models
from account.models import group, AccountUser

# Create your models here.
class Shift(models.Model):
    Shift_id = models.AutoField(primary_key=True)
    group_name = models.ForeignKey(group, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    num_hours = models.IntegerField()
    num_people = models.IntegerField()
    
    def __str__(self):
        return f"Shift ID: {self.Shift_id}, Group: {self.group_name}, Start Time: {self.start_time}, Num Hours: {self.num_hours}, Num People: {self.num_people}"
    
class ShiftUser(models.Model):
    shift_id = models.ForeignKey(Shift, on_delete=models.CASCADE)
    user_id = models.ForeignKey(AccountUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"Shift ID: {self.shift_id}, User ID: {self.user_id}"