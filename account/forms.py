from django import forms

class LoginForm(forms.Form):
    users_id = forms.CharField(label="User ID", max_length=20)
    password = forms.CharField(label="Password", max_length=20, widget=forms.PasswordInput)