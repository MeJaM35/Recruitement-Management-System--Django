from django.core.mail import send_mail
from django.shortcuts import render, redirect
from .models import User, Applicant, Skill, Edu, Exp, Organization, Recruiter
from .forms import UserSignUpForm, ApplicantForm, ProfileForm, EduForm, ExpForm, OrgForm, AdminForm, RecruiterForm
from django.contrib import messages
from django.contrib.auth import login, logout , authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect 





def register_org(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = OrgForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            org = form.save()
            return redirect('register-admin', org.id)

    context = {
        'form' : form,
    }

    return render(request, 'base/org_create.html', context)


def register_admin(request,pk):
    form = AdminForm(request.POST)
    if request.user.is_authenticated:
        return redirect('home')
    org = Organization.objects.get(id=pk)
    if form.is_valid():
            user = form.save(commit=False)
            user.role = 'admin'
            user.email = org.email
            user.username = org.name+"_admin"
            user.save()
            org.admin = user
            org.is_activated = True
            org.save()
            login(request, user)
            return redirect('home')
            

    context = {
       'form': form,
    }

    return render(request, 'base/admin-register.html', context)


@login_required(login_url='login')
def add_recruiter(request):
    Org = Organization.objects.get(admin=request.user)
    if request.user.role == 'admin':
        form = RecruiterForm(request.POST)
        if request.method == 'POST':        # For 'POST' request
            form = RecruiterForm(request.POST)
            if form.is_valid():
                rec = form.save(commit=False)
                rec.role = 'Applicant'
                rec.save()
                recu = Recruiter.objects.create(
                    User = rec,
                    role = 'recruiter',

                )
                Org.recruiters.add(recu)
                send_mail(
    f'Login to your Recruiter Acc at {Org}',
    f'Your Username = email. this email, password = {request.POST.get("password1")}',
    'mj@sertibots.com',
    [f'{rec.email}'],
)
                redirect('home')

    context  = {
        'form': form,
    }

    return render(request, 'base/add-recruiter.html', context)






def register(request):
    form = UserSignUpForm()
    if request.method == 'POST':        # For 'POST' request
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'Applicant'
            user.save()
            login(request, user)
            messages.success(
                request, f'Your account has been created! You are now logged in!')
            if user.role == 'Applicant':
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
    Skills = Skill.objects.filter(applicant = User.applicant)
    edu = Edu.objects.filter(applicant = User.applicant)
    exp = Exp.objects.filter(applicant = User.applicant)
    
    context = {
        'User' : User,
        'Skills' : Skills,
        'Edu' : edu,
        'exp': exp,

    }
    return render(request, 'base/applicant-details.html', context)


@login_required(login_url='login')
def add_edu(request):
    User =request.user
    edu = Edu.objects.filter(applicant = User.applicant)
    form = EduForm(request.POST)
    if request.method == 'POST':
       edu = form.save()
       User.applicant.edu.add(edu)


       return redirect('view-profile')
   

        


    context = {
        'User': User,
        'form': form,
        'edu': edu,
    }
    return render(request, 'base/add-edu.html', context)


@login_required(login_url='login')
def add_exp(request):
    User =request.user
    exp = Exp.objects.filter(applicant = User.applicant)
    form = ExpForm(request.POST)
    if request.method == 'POST':
       exp = form.save()
       User.applicant.exp.add(exp)


       return redirect('view-profile')
   

        


    context = {
        'User': User,
        'form': form,
        'exp': exp,
    }
    return render(request, 'base/add-exp.html', context)

@login_required(login_url='login')
def add_skills(request):
    page = 'add_skill'
    User =request.user
    Skills = Skill.objects.filter(applicant = User.applicant)
    if request.method == 'POST':
        skill = Skill.objects.create(
            name = request.POST.get('skill'),
        )
        User.applicant.skills.add(skill)


        return redirect('view-profile')
   

        


    context = {
        'User': User,
        'Skills': Skills,
    }
    return render(request, 'base/add-skills.html', context)

@login_required(login_url='login')
def user_edit(request, pk):
    user = User.objects.get(id=pk)
    form = ProfileForm(instance=user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('view-profile')
   

        


    context = {
        'pform': form,
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
    user = request.user
    context = {
        'user': user,
    }
    return render(request, 'base/home.html', context) 
# Create your views here.

def contact(request):
   
    return render(request, 'base/contact.html', context={}) 

def about(request):
    return render(request, 'base/about.html', context={}) 


