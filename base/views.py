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
                return redirect('applicant-details')
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
def view_profile(request):
    User = request.user
    context = {
        'User' : User,

    }
    return render(request, 'base/applicant-details.html', context)

@login_required(login_url='login')
def user_edit(request, pk):
    user = User.objects.get(id=pk)
    pform = ProfileForm(instance=request.user)
    if request.method == 'POST':
        #user.pfp = request.FILES
        user.username = request.POST.get('username')
        user.fname = request.POST.get('first_name')
        user.lname = request.POST.get('last_name')
        user.save()
        return redirect('view-profile')

        


    context = {
        'pform': pform,
    }
    return render(request, 'base/user-edit.html', context)

@login_required(login_url='login')
def applicant_edit(request):

    form = ApplicantForm()
    User = request.user

    if request.method == 'POST':
        Applicant.objects.update_or_create(

            User = User,
            about = request.POST.get('about'),
            age = request.POST.get('age'),
            pronouns = request.POST.get('pronouns'),
            location = request.POST.get('location'),
            resume = request.POST.get('resume'),

        )
        return redirect('view-profile')
        


    context = {
        'form': form,
    }
    return render(request, 'base/applicant-edit.html', context)
          


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