from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pfp = models.ImageField(upload_to='pfps', null=True, blank=True, default='user-regular.svg')
    username = models.CharField(max_length=20, null=True)
    email = models.EmailField(unique=True, null=True)
    fname = models.CharField(max_length=20, null=True)
    lname = models.CharField(max_length=20, null=True)
    phone = models.BigIntegerField(null=True)
    is_applicant = models.BooleanField(default=True)
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

class Edu(models.Model):
        degree = models.CharField(max_length=20, null=True)
        inst = models.CharField(max_length=20, null=True)
        start_date = models.DateField(null=True)
        end_date = models.DateField(null=True)
        skills = models.ManyToManyField(Skill, blank=True)
        grade = models.IntegerField(null=True, blank=True)
        credentials = models.URLField(blank=True)


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
        return self.User.username
    







# class Recruiter(models.Model):
#     User = models.ForeignKey(User, null=True, on_delete= models.CASCADE)
#     role = models.CharField(max_length=50, null=True)

#     def __str__(self):
#         return 'r'+self.User.username

# class Organization(models.Model):
#     name = models.CharField(max_length=50, null=True)
#     logo = models.ImageField(upload_to='pfps', null=True, blank=True, default='default.jpg')
#     admin = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
#     email = models.EmailField(null=True, unique=True)
#     website = models.URLField(null=True, blank=True)
#     recruiters = models.ManyToManyField(Recruiter, blank=True, related_name='org', on_delete=models.CASCADE)

#     def __str__(self):
#         return self.name


# Create your models here.
