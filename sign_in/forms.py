from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

class SignInViaUsernameForm(forms.Form):
    username = forms.CharField(label="username",max_length=25)
    password = forms.CharField(label=('Password'), max_length=25, widget=forms.PasswordInput)

    def login(self):
                 #get and clean the username and password input
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            #authenticate user using cleaned username and password
            user = authenticate(request, username=username, password=password)
        

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class createUserForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Required. Enter your first name.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required. Enter your last name.')
    email = forms.EmailField(max_length = 200) 
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name','email', 'password1', 'password2')

    def createUser(self, commit=True):
        user = super(createUserForm, self).save(commit=False)  # Use the correct class name
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user 



        
    