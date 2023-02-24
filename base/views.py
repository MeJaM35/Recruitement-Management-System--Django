import email
from django.shortcuts import render, redirect
from .models import User, Applicant
from .forms import UserSignUpForm, ApplicantForm, ProfileForm
from django.contrib import messages
from django.contrib.auth import login, logout , authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect 




def register(request):
    form = UserSignUpForm()
    if request.method == 'POST':        # For 'POST' request
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_Applicant = True
            user.save()
            login(request, user)
            messages.success(
                request, f'Your account has been created! You are now logged in!')
            if user.is_Applicant:
                return redirect('applicant-edit')
        else:
            form = UserSignUpForm(request.POST)
            messages.error(request, 'An error occurred during registration')
            return redirect('register')
    else:                            # Else for 'GET' request
        form = UserSignUpForm()
    context = {
        'form' : form,
    }
    return render(request, 'base/register.html', context)

@login_required(login_url='login')
def applicant_edit(request):
    User = request.user
    form2 = ApplicantForm(request.POST)
    form1 = ProfileForm(request.POST, instance=User)
    try:
        applicant = Applicant.objects.get(User=User)
    except:

            if request.method == 'POST':
                
                if form2.is_valid() and form1.is_valid():
                    User = form1.save()

                    applicant = form2.save(commit=False)
                    print(applicant)
                    Applicant.objects.create(User=User,
                    about = form2.about,
                    pronouns = form2.pronouns,
                    age = form2.age,
                    location = form2.location,
                    resume = form2.resume,


                    
                    )
                    

                    return redirect('applicant-edit')

    context = {
        'form2': form2,
        'form1': form1,

    
    }

    return render(request, 'base/profile.html', context)


def loginUser(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exit')

    context = {'page': page}
    return render(request, 'base/login.html', context)

@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('home')

def home(request):
    return render(request, 'base/home.html', context={}) 
# Create your views here.

def contact(request):
    return render(request, 'base/contact.html', context={}) 

def about(request):
    return render(request, 'base/about.html', context={}) 