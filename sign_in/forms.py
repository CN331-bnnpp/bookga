from django import forms
from django.contrib.auth import authenticate, login
from django.contrib import messages


class SignInViaUsernameForm(forms.Form):
    username = forms.CharField(label="Username", max_length=25)
    password = forms.CharField(label="Password", max_length=25, widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)

            if user is None:
                raise forms.ValidationError('Invalid username or password.')

            if not user.is_active:
                raise forms.ValidationError('This account is inactive.')

            self.user_cache = user

        return cleaned_data

    def login(self, request):
        if hasattr(self, 'user_cache'):
            login(request, self.user_cache)
            messages.success(request, "Login success!")
    


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
        user.is_staff = True
        if commit:
            user.save()
        return user 
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email
    


