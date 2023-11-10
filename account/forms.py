from django.contrib.auth.forms import UserCreationForm
from .models import AccountUser

class CreateAccountForm(UserCreationForm):
    class Meta:
        model = AccountUser
        fields = ("username", "email", "password1", "password2")
        
    def save(self, commit=True):
        user = super(CreateAccountForm, self).save(commit=False)
        if commit:
            user.save()
        return user