from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
    
class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    is_staff = True
    
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "password1", "password2"]
        
    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.users_id = self.generate_users_id()
        user.username = self.cleaned_data["username"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.is_staff = self.is_staff
        
        if commit:
            user.save()
            
        return user

    def generate_users_id(self):
        """
        Generates a unique users_id for a new user.
        """
        users_id = f"{User.objects.count() + 1:06d}" 
        return users_id