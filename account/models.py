from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class AccountUser(AbstractUser):

    class Meta(AbstractUser.Meta):
        swappable = "AUTH_USER_MODEL"

class group(models.Model):
    """
    A model representing a group of users.
    """
    username = models.ForeignKey(AccountUser, on_delete=models.CASCADE, limit_choices_to={"is_staff": True})
    group_name = models.CharField(max_length=20, primary_key=True)
        
    def __str__(self):
        return f"{self.username} {self.group_name}"
        
    def get_group_name(self):
        return self.group_name
        
class group_member(models.Model):
    """
    A model representing a group member, linking a user to a group.
    """
    username = models.ForeignKey(AccountUser, on_delete=models.CASCADE, limit_choices_to={"is_staff": False})
    group_name = models.ForeignKey(group, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.username} {self.group_name}"
    
    def get_group_name(self):
        return self.group_name
        