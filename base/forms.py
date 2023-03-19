from django import forms
from django.forms import ModelForm
from .models import User, Applicant, Edu, Exp, Organization, Recruiter
from django.contrib.auth.forms import UserCreationForm


class UserSignUpForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'password1': forms.PasswordInput(attrs={'placeholder': 'Password'}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),
        }



class ProfileForm(ModelForm):
    class Meta:
        model = User
        fields = ['pfp', 'username', 'first_name', 'last_name']




class ApplicantForm(ModelForm):
    class Meta:
        model = Applicant
        fields = ['about', 'age', 'pronouns', 'location', 'resume',  ]


class EduForm(ModelForm):
    class Meta:
        model = Edu
        fields = ['degree', 'inst', 'start_date', 'end_date', 'grade', 'credentials'  ]


class ExpForm(ModelForm):
    class Meta:
        model = Exp
        fields = ['role', 'company', 'start_date', 'end_date'  ]


class OrgForm(ModelForm):
    class Meta:
        model = Organization
        fields = ['name', 'email', 'website'  ]


class AdminForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'password1', 'password2']


class RecruiterForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'phone', 'password1', 'password2']

