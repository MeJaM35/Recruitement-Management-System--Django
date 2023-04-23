from django import forms
from django.forms import ModelForm, DateInput
from .models import User, Applicant, Edu, Exp, Organization, Recruiter, Job, Skill
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
        fields = ['pfp', 'username', 'fname', 'lname']




class ApplicantForm(ModelForm):
    class Meta:
        model = Applicant
        fields = ['about', 'age', 'pronouns', 'location', 'resume'  ]


class EduForm(ModelForm):
    start_date = forms.DateField(widget=DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Edu
        fields = ['degree', 'inst', 'start_date', 'end_date', 'grade', 'credentials']
        widgets = {
            'start_date': DateInput(attrs={'type': 'date'}),
            'end_date': DateInput(attrs={'type': 'date'}),
        }
        input_formats = {
            'start_date': ['%Y-%m-%d'],
            'end_date': ['%Y-%m-%d'],
        }



class ExpForm(ModelForm):
    class Meta:
        model = Exp
        fields = ['role', 'company', 'start_date', 'end_date'  ]


class OrgForm(ModelForm):
    class Meta:
        model = Organization
        fields = ['name', 'email', 'website'  ]

        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Organization Name'}),
            'website': forms.TextInput(attrs={'placeholder': 'Website'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
        }


class AdminForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'password1', 'password2']

        widgets = {
            
            'first_name': forms.TextInput(attrs={'placeholder': 'Fir Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
            
            'password1': forms.PasswordInput(attrs={'placeholder': 'Password'}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),
        }


class RecruiterForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'phone', 'password1', 'password2']


class JobForm(ModelForm):
    class Meta:
        model = Job
        fields = ['position', 'start_date', 'pay_range', 'description', 'skills_req', 'edu_req', 'exp_req'  ]

        widgets = {
            'position': forms.TextInput(attrs={'placeholder': 'Position'}),
            'stat_date': forms.DateInput(attrs={
                'type': 'date', 'placeholder': 'yyyy-mm-dd',
                'class': 'form-control'
                }),
            'pay_range': forms.NumberInput(attrs={'placeholder': 'eg. 10000'}),
            'description': forms.Textarea(attrs={'placeholder': 'description here'}),
            # 'skills_req': forms.SelectMultiple(),
            # 'edu_req': forms.SelectMultiple(),
            # 'exp_req': forms.SelectMultiple(),

        }

class LinkForm(ModelForm):
    class Meta:
        model = Applicant
        fields = ('github', 'linkedin')


