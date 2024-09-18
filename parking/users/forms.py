from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Profile

class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=100, required=True, widget=forms.TextInput())
    email = forms.EmailField(max_length=100, required=True, widget=forms.EmailInput())
    password1 = forms.CharField(max_length=100, required=True, widget=forms.PasswordInput())
    password2 = forms.CharField(max_length=100, required=True, widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email address already exists.")
        return email

class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']

class ProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput())

    class Meta:
        model = Profile
        fields = ['avatar']
