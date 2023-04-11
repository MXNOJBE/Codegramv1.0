from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class StudentSignupForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Enter a valid email address.')
    username = forms.CharField(max_length=30, required=True, help_text='Required. Enter a username.')
    first_name = forms.CharField(max_length=30, required=True, help_text='Required. Enter your first name.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required. Enter your last name.')
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

class RecruiterSignupForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Enter a valid email address.')
    username = forms.CharField(max_length=30, required=True, help_text='Required. Enter a username.')
    first_name = forms.CharField(max_length=100, required=True, help_text='Required. Enter the name of your company.')
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'password1', 'password2')
