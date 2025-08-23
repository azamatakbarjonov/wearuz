from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ["username", "email", "phone", "address", "avatar", "password1", "password2"]

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username yoki Email")
    password = forms.CharField(widget=forms.PasswordInput)

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["username", "email", "phone", "address", "avatar"]

from django import forms
from django.contrib.auth.forms import AuthenticationForm

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        "class": "w-full p-3 rounded-lg bg-white/20 text-white outline-none",
        "placeholder": "Username yoki Email"
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "w-full p-3 rounded-lg bg-white/20 text-white outline-none",
        "placeholder": "Parol"
    }))