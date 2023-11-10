from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    """
    A custom user model that extends the built-in Django `AbstractUser` model.
    Includes an additional `users_id` field that serves as the primary key.
    """
    users_id = models.CharField(max_length=20, primary_key=True)

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
        
    def __str__(self):
        return f"{self.users_id} {self.get_full_name()}"
    
    def get_user_id(self):
        return self.users_id
    
class group(models.Model):
    """
    A model representing a group of users.
    """
    users_id = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={"is_staff": True})
    group_name = models.CharField(max_length=20, primary_key=True)
        
    def __str__(self):
        return f"{self.users_id} {self.group_name}"
        
    def get_group_name(self):
        return self.group_name
        
class group_member(models.Model):
    """
    A model representing a group member, linking a user to a group.
    """
    users_id = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={"is_staff": False})
    group_name = models.ForeignKey(group, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.users_id} {self.group_name}"
    
    def get_group_name(self):
        return self.group_name
        