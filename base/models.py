from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
from phonenumber_field.modelfields  import PhoneNumberField


ROLE_CHOICES = (
    ('admin', 'admin'),
    ('recruiter', 'recruiter'),
    ('applicant', 'applicant'),
)

STATUS_CHOICES = (
    ('not_applied', 'not_applied'),
    ('applied', 'applied'),
    ('shortlisted', 'shortlisted'),
    ('interviewed', 'interviewed'),
    ('rejected', 'rejected'),
    ('accepted', 'accepted'),
)


class User(AbstractUser):
    pfp = models.ImageField(upload_to='pfps', null=True, blank=True, default='user-regular.svg')
    username = models.CharField(max_length=50, null=True)
    email = models.EmailField(unique=True, null=True)
    fname = models.CharField(max_length=20, null=True)
    lname = models.CharField(max_length=20, null=True)
    phone = models.PhoneNumberField(null=True)
    role = models.CharField(max_length = 50, choices = ROLE_CHOICES, default='applicant')
    #bio = models.TextField(blank=True, null=True)
    #pronouns = models.CharField(max_length=10, null=True, blank=True)
    ##pfp = models.ImageField(upload_to='pfps', null=True, blank=True, default='default.jpg')
    #is_writer = models.BooleanField(null=True, default=False)

    

    def __str__(self):
        return self.username

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username']


class Skill(models.Model):
        name = models.CharField(max_length=20, null=True)
        def __str__(self):
            return self.name


class Exp(models.Model):
        role = models.CharField(max_length=20, null=True)
        company = models.CharField(max_length=20, null=True)
        start_date = models.DateField(null=True)
        end_date = models.DateField(null=True)
        skills = models.ManyToManyField(Skill, blank=True)

        def __str__(self):
            return str(self.role)

class Edu(models.Model):
        degree = models.CharField(max_length=20, null=True)
        inst = models.CharField(max_length=20, null=True)
        start_date = models.DateField(null=True)
        end_date = models.DateField(null=True)
        skills = models.ManyToManyField(Skill, blank=True)
        grade = models.IntegerField(null=True, blank=True)
        credentials = models.URLField(blank=True)

        def __str__(self):
            return str(self.degree)


class Applicant(models.Model):
    User = models.OneToOneField(User, null=True, related_name='applicant', on_delete=models.CASCADE)
    about = models.TextField(blank=True, null=True)
    age = models.IntegerField(null=True)
    pronouns = models.CharField(max_length=10, null=True)
    location = models.CharField(max_length=10, null=True)
    resume = models.FileField(upload_to='resume', null=True)
    skills = models.ManyToManyField(Skill, blank=True)
    exp = models.ManyToManyField(Exp, blank=True)
    edu = models.ManyToManyField(Edu, blank=True)

    def __str__(self):
        return str(self.User.username)
    







class Recruiter(models.Model):
    User = models.OneToOneField(User, null=True, on_delete= models.CASCADE, related_name='recruiters')
    role = models.CharField(max_length=50, null=True)



class Organization(models.Model):
    name = models.CharField(max_length=50, null=True)
    logo = models.ImageField(upload_to='pfps', null=True, blank=True, default='default.jpg')
    admin = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    email = models.EmailField(null=True, unique=True)
    website = models.URLField(null=True, blank=True)
    recruiters = models.ManyToManyField(Recruiter, blank=True, related_name='org')
    activated = models.BooleanField(default=False)

    def __str__(self):
         return str(self.name)

class Job(models.Model):
    Org = models.ForeignKey(Organization, related_name='org', on_delete=models.CASCADE)
    Recruiter = models.ForeignKey(Recruiter, related_name='recruiter', on_delete=models.CASCADE)
    position = models.CharField(max_length=20, null=True)
    created = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField(default=datetime.now())
    pay_range = models.IntegerField()
    description = models.TextField(null=True)
    skills_req = models.CharField(max_length=50, blank=True, null = True)
    exp_req = models.CharField(max_length=50, blank=True, null = True)
    edu_req = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default= True)

    def __str__(self):
            return str(self.position)
    

class Application(models.Model):
    applicant = models.ForeignKey(Applicant, null=True, blank=True, related_name='app', on_delete=models.SET_NULL)
    job = models.ForeignKey(Job, null=True, blank=True, related_name='app', on_delete=models.SET_NULL)
    status = models.CharField(max_length = 50, choices = STATUS_CHOICES, default='not_applied')





# Create your models here.
