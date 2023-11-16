from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import AccountUser

class CreateAccountForm(UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        help_text="Password must be at least 8 characters long.",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'type':'password', 'align':'center', 'placeholder':'Password'}),
    )
    password2 = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'type':'password', 'align':'center', 'placeholder':'Password'}),
    )
    class Meta:
        model = AccountUser
        fields = ("username", "email", "password1", "password2")
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        }
        
    def save(self, commit=True):
        user = super(CreateAccountForm, self).save(commit=False)
        if commit:
            user.save()
        return user