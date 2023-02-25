from django import forms
from django.forms import ModelForm
from .models import User, Applicant
from django.contrib.auth.forms import UserCreationForm


class UserSignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class ProfileForm(ModelForm):
    class Meta:
        model = User
        fields = ['pfp', 'username', 'first_name', 'last_name']




class ApplicantForm(ModelForm):
    class Meta:
        model = Applicant
        fields = ['about', 'age', 'pronouns', 'location', 'resume',  ]