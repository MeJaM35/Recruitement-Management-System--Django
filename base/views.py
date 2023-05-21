from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from .models import User, Applicant, Skill, Edu, Exp, Organization, Recruiter, Job, Application, Interview
from .forms import UserSignUpForm, ApplicantForm, ProfileForm, EduForm, ExpForm, OrgForm, AdminForm, RecruiterForm, JobForm, LinkForm, InterviewForm
from django.contrib import messages
from django.contrib.auth import login, logout , authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.core.mail import EmailMessage, get_connection
from datetime import datetime
from django.views import View
from django.conf import settings
from verify_email.email_handler import send_verification_email




def cgpa(cgpa):
    if int(cgpa) <= 10:
        return int(cgpa)
    else:
        cgpa = int(cgpa) / 10
        return int(cgpa)


@login_required(login_url='login')
def addLinks(request):
    user = request.user
    Org = None
    if user.role == 'admin':
        Org = Organization.objects.get(admin = user)

    try:
        # Try to retrieve an existing object associated with the user
        instance = Applicant.objects.get(User=user)
        is_update = True
    except Applicant.DoesNotExist:
        # If the object does not exist, create a new one
        instance = Applicant(User=user)
        is_update = False

    if request.method == 'POST':
        form = LinkForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        form = LinkForm(instance=instance)

    context = {
        'form' : form,
        'is_update': is_update ,
        'Org': 'Org' # Pass a flag indicating if it's an update or not
    }
    return render(request, 'base/add-links.html', context)



class PDFView(View):
    def get(self, request, pk):
        # Retrieve the Applicant instance
        applicant = get_object_or_404(Applicant, id=pk)

        # Retrieve the file path of the resume field
        resume_file_path = applicant.resume.path

        # Open the resume file in binary mode
        with open(resume_file_path, 'rb') as resume_file:
            # Read the file content
            resume_content = resume_file.read()

            # Create an HttpResponse object with the resume content
            response = HttpResponse(resume_content, content_type='application/pdf')

            # Add the Content-Disposition header to indicate inline display
            response['Content-Disposition'] = 'inline; filename=my_resume.pdf'

            return response




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
                rec.role = 'recruiter'
                rec.save()
                recu = Recruiter.objects.create(
                    User = rec,
                    role = 'recruiter',

                )
                Org.recruiters.add(recu)
                return redirect('home')
                
                # connection = get_connection()
                # with connection as connection:

                #     message = '''
                #             Hey {rec.User.username}, here's your {rec.User.org} Recruiter
                #             Use your email with password: {request.POST.get('password1')}
                #             '''
                #     Email = EmailMessage('Heres your email',message,'mj@sertibots.com',rec.email,connection=connection)
                #     Email.send()
                #     connection.close()
                
                

    context  = {
        'form': form,
        'Org': Org,
    }

    return render(request, 'base/add-recruiter.html', context)






def register(request):
    form = UserSignUpForm()
    if request.method == 'POST':        # For 'POST' request
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'applicant'
            user.save()
            if user.role == 'applicant':
                Applicant.objects.create(User=user)
                inactive_user = send_verification_email(request, form)
                return HttpResponseRedirect('https://mail.google.com/')        
        else:
            form = UserSignUpForm(request.POST)
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field.title()}: {error}')           
            return redirect('register')
    else:                            # Else for 'GET' request
        form = UserSignUpForm()
    context = {
        'form' : form,
    }
    return render(request, 'base/register.html', context)



        
    


@login_required(login_url='login')
def view_profile(request, pk):
    Org = None
    if request.user.role == 'admin':
        Org = Organization.objects.get(admin = request.user)
    user = User.objects.get(id=pk)
    Skills = Skill.objects.filter(applicant = user.applicant)
    edu = Edu.objects.filter(applicant = user.applicant)
    exp = Exp.objects.filter(applicant = user.applicant)
    
    context = {
        'User' : user,
        'Skills' : Skills,
        'Edu' : edu,
        'exp': exp,
        'Org': Org

    }
    return render(request, 'base/applicant-details.html', context)


@login_required(login_url='login')
def add_edu(request):
    User =request.user
    edu = Edu.objects.filter(applicant = User.applicant)
    form = EduForm(request.POST)
    if request.method == 'POST':
       edu = form.save(commit=False)
       edu.grade = cgpa(edu.grade)
       edu.save()
       User.applicant.edu.add(edu)


       return redirect('view-profile', User.id)
   

        


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


       return redirect('view-profile', User.id)
   

        


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
        skill, created = Skill.objects.get_or_create(name=request.POST.get('name'))
        User.applicant.skills.add(skill)


        return redirect('view-profile', User.id)
   

        


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
            return redirect('view-profile', user.id)
   

        


    context = {
        'pform': form,
    }
    return render(request, 'base/user-edit.html', context)

@login_required(login_url='login')
def applicant_edit(request):
    user = request.user
    applicant = Applicant.objects.get(User=user)
    form = ApplicantForm(request.POST, instance=applicant)

    if request.method == 'POST':
        form = ApplicantForm(request.POST, instance=applicant)
        applicant.location = request.POST.get('location')
        applicant.pronouns = request.POST.get('pronouns')
        applicant.age = request.POST.get('age')

        applicant.about = request.POST.get('about')
        applicant.resume = request.POST.get('resume')
        applicant.save()
        return redirect('view-profile', user.id)
    else:
        form = ApplicantForm(request.POST, instance=applicant)
    context = {
        'form': form,
        'User': user,
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
    Org = None
    
    context = {
        'user': user,
        'Org': Org,
    }
    if user.is_authenticated:

        if user.role == 'admin':
            Org = Organization.objects.get(admin = user)
        
        if user.role == 'applicant':
            job = Job.objects.filter(is_active = True)
            context['job'] = job
        if user.role == 'recruiter':
            job = Job.objects.filter(Recruiter = user.recruiters )
            context['job'] = job
        if user.role == 'admin':
            org = Organization.objects.get(admin=user)
            recruiter = Recruiter.objects.filter(org=org)
            context['recruiter'] = recruiter
            
    else:
        job = Job.objects.all()
        context['job'] = job

    
    
    return render(request, 'base/home.html', context) 




@login_required(login_url='login')
def jobdetails(request,pk):
    user = request.user
    Org = None
    if user.role == 'admin':
        Org = Organization.objects.get(admin = user)
    if user.role == 'recruiter':
        job = Job.objects.get(id = pk)
        apps = Application.objects.filter(job=job)

    context = {
        'apps' : apps,
        'Org': Org,
    }

    return render(request, 'base/job-details.html', context)

@login_required(login_url='login')
def closejob(request, pk):
    user = request.user
    
    if user.role == 'recruiter':
        job = Job.objects.get(id = pk)
        job.is_active = False
        job.save()
        return redirect(request.META.get('HTTP_REFERER')) 
    
    return redirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='login')
def activatejob(request, pk):
    user = request.user
    if user.role == 'recruiter':
        job = Job.objects.get(id = pk)
        job.is_active = True
        job.save()
        return redirect(request.META.get('HTTP_REFERER')) 
    
    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def shortlist(request, pk):
    user = request.user
    context = {'user': user}
    if user.role == 'recruiter':
        app = Application.objects.get(id=pk)
        app.status = "shortlisted"
        app.save()
        context['app'] = app
         # email functionality
        applicant = app.applicant
        recipient = applicant.User.email
        subject = 'Your job application has been accepted!'
        message = f'Hi {applicant.User.fname},\n\nWe are pleased to inform you that your job application at {app.job.Org.name} for {app.job.position} has been {app.status}. Please contact us at {settings.DEFAULT_FROM_EMAIL} to schedule the next steps of the hiring process.\n\nBest regards,\nThe Hiring Team'
        sender = settings.DEFAULT_FROM_EMAIL
        send_mail(
            subject,
            message,
            sender,
            [recipient],
            fail_silently=False,
        )
        return redirect(request.META.get('HTTP_REFERER'))

    return redirect(request.META.get('HTTP_REFERER'))





@login_required(login_url='login')
def accept(request, pk):
    user = request.user
    context = {'user': user}
    if user.role == 'recruiter':
        app = Application.objects.get(id=pk)
        if app.status == 'interviewed':
            app.status = "accepted"
            app.save()
            context['app'] = app
            # email functionality
            applicant = app.applicant
            recipient = applicant.User.email
            subject = 'Your job application has been accepted!'
            message = f'Hi {applicant.User.fname},\n\nWe are pleased to inform you that your job application at {app.job.Org.name} for {app.job.position} has been {app.status}. Please contact us at {settings.DEFAULT_FROM_EMAIL} to schedule the next steps of the hiring process.\n\nBest regards,\nThe Hiring Team'
            sender = settings.DEFAULT_FROM_EMAIL
            send_mail(
                subject,
                message,
                sender,
                [recipient],
                fail_silently=False,
            )
        return redirect(request.META.get('HTTP_REFERER'))

    return redirect(request.META.get('HTTP_REFERER'))




@login_required(login_url='login')
def reject(request, pk):
    user = request.user
    context = {'user': user}
    if user.role == 'recruiter':
        app = Application.objects.get(id=pk)
        if app.status == 'interviewed':
            app.status = "rejected"
            app.save()
            context['app'] = app
             # email functionality
            applicant = app.applicant
            recipient = applicant.User.email
            subject = 'Your job application has been accepted!'
            message = f'Hi {applicant.User.fname},\n\nWe are pleased to inform you that your job application at {app.job.Org.name} for {app.job.position} has been {app.status}. Please contact us at {settings.DEFAULT_FROM_EMAIL} to schedule the next steps of the hiring process.\n\nBest regards,\nThe Hiring Team'
            sender = settings.DEFAULT_FROM_EMAIL
            send_mail(
                subject,
                message,
                sender,
                [recipient],
                fail_silently=False,
            )
        return redirect(request.META.get('HTTP_REFERER'))

    return redirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='login')
def interview(request, pk):
    user = request.user
    context = {'user': user}
    if user.role == 'recruiter':
        app = Application.objects.get(id=pk)
        form = InterviewForm()
        context['form'] = form

        if request.method == 'POST':
        
            form = InterviewForm()
            context['form'] = form

            date = request.POST.get('date')
            time = request.POST.get('time')
            interview = Interview.objects.create(date=date, time=time, application=app)
            
            context['app'] = app
            applicant = app.applicant
            recipient = applicant.User.email
            subject = 'Your job application has been accepted!'
            message = f'Hi {applicant.User.fname},\n\nWe are pleased to inform you that your job application at {app.job.Org.name} for {app.job.position} has been scheduled for an interview on {app.app.time} at {app.app.date}. Please Login to your account to get the meeting link.\n\nBest regards,\nThe Hiring Team'
            sender = settings.DEFAULT_FROM_EMAIL
            send_mail(
                subject,
                message,
                sender,
                [recipient],
                fail_silently=False,
            )
            app.status = "interviewed"
            app.save()
            return redirect(request.META.get('HTTP_REFERER'))

    return render(request, 'base/interview.html', context)










@login_required(login_url='login')
def addJob(request):
    User = request.user
    Org = None
    if User.role == 'admin':
        Org = Organization.objects.get(admin = User)
    print(User.recruiters.org)
    form = JobForm()

    if request.method == 'POST':
        # print('post request')
        # if form.is_valid():
            print('post request')
            job = Job.objects.create(
                Org = Organization.objects.get(recruiters = User.recruiters),
               Recruiter = User.recruiters,
                position = request.POST.get('position'),
                start_date = request.POST.get('start_date'),
                pay_range = request.POST.get('pay_range'),
                description = request.POST.get('description'),
                grade_req = cgpa(request.POST.get('grade_req')),
                exp_req = request.POST.get('exp_req'),
                edu_req = request.POST.get('edu_req'),
                met_req = request.POST.get('met_req') == 'on',

               


            )
            job.skills_req.add(request.POST.get('skills_req'))
            job.save()
            
            
            return redirect('home')

    context = {
        'form': form,
        'Org': Org,
    }


    return render(request, 'base/add-job.html', context)
# Create your views here.

def chat(request):
    return render(request, "base/chat.html")

def room(request, room_name):
    return render(request, "base/chat-room.html", {"room_name": room_name})

def contact(request):
   
    return render(request, 'base/contact.html', context={}) 

def about(request):
    return render(request, 'base/about.html', context={}) 



@login_required(login_url='login')
def notif(request):
    user = request.user
    Org = None
    if user.role == 'admin':
        Org = Organization.objects.get(admin = user)
    context = {
        'Org': Org,
    }
    if user.role == 'applicant':
        App = Application.objects.filter(applicant=user.applicant)
        context['app'] = App    
        job_statuses = [(app.job.position, Application.status) for app in App]
        context['job_statuses'] = job_statuses 
        applied_count = Application.objects.filter(status='applied').count()
        context['applied_count']= applied_count
        applied_count = Application.objects.filter(status='shortlisted').count()
        context['shortlisted_count']= applied_count
        applied_count = Application.objects.filter(status='rejected').count()
        context['rejected_count']= applied_count
        applied_count = Application.objects.filter(status='interviewed').count()
        context['interviewed_count']= applied_count
         
        
    return render(request, 'base/notif.html', context)


@login_required(login_url='login')
def Apply(request, pk):
    user = request.user
    
    job = Job.objects.get(id=pk)
    if user.role == 'applicant':
        app = Applicant.objects.get(User = user)

        try:
            appl = Application.objects.get(job=job, applicant = app)
            return redirect('ERROR')
        except:

            if job.met_req:
                print('passed met req')

                min_req = job.edu_req
                edu = get_object_or_404(Edu, applicant = app, level = min_req)
                if min_req == edu.level:
                    print('passed level')
                    if edu.grade >= job.grade_req:
                        print('passed grade')
                        application = Application.objects.create(
                        job = job,
                        applicant = app,
                        status = 'applied',
                        )
                    else:
                        return redirect('ERROR')

                
                
            else:
                    application = Application.objects.create(
                    job = job,
                    applicant = app,
                    status = 'applied',
                    )
                    return redirect('notif')
    return render(request, 'base/desc.html')


def desc(request,pk):
    job = Job.objects.get(id=pk)
    user = request.user
    skills= Skill.objects.filter(job=job)
    context = {
        'job': job,
        'skills' : skills,
    }


    return render(request, 'base/desc.html', context) 

@login_required(login_url='login')
def dashboard(request,pk):
    user = request.user
    rec = Recruiter.objects.get(pk=pk)
    filter_param = request.GET.get('filter')

    context = {
        'user': user,
        'rec': rec,
    }
    if user.role == 'admin':
        job = Job.objects.filter(Recruiter = rec)
        if filter_param == 'all':
        # Filter for all records
            job = Job.objects.filter(Recruiter = rec)
        elif filter_param == 'active':
            # Filter for active records
            job = Job.objects.filter(Recruiter = rec, is_active = True)
        elif filter_param == 'passive':
            # Filter for passive records
            job = Job.objects.filter(Recruiter = rec, is_active = False)
        else:
            # Default filter option (if none selected)
            job = Job.objects.filter(Recruiter = rec)
        context['job'] = job

    return render(request, 'base/recruiter-details.html', context)

@login_required(login_url='login')
def get_apps(request,pk, *args, **kwargs): 
    user = request.user
    rec = Recruiter.objects.get(id=pk)
    job = Job.objects.get(id=kwargs.get('id'))
    apps = Application.objects.filter(job = job)

    status = request.GET.get('filter')
    
    # Filter applications based on selected status
    if status == 'all':
        apps = Application.objects.filter(job=job)
    elif status == 'applied':
        apps = Application.objects.filter(job=job, status='applied')
    elif status == 'shortlisted':
        apps = Application.objects.filter(job=job, status='shortlisted')
    elif status == 'interviewed':
        apps = Application.objects.filter(job=job, status='interviewed')
    elif status == 'accepted':
        apps = Application.objects.filter(job=job, status='accepted')
    elif status == 'rejected':
        apps = Application.objects.filter(job=job, status='rejected')
    else:
                apps = Application.objects.filter(job=job)



    context= {
        'user': user,
        'rec' : rec,
        'job' : job,
        'apps': apps
    }
    return render(request, 'base/applications.html', context)

    


def ERROR(request):
    return render(request,"base/notq.html")



