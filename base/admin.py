from django.contrib import admin
from .models import User, Exp, Edu, Skill, Applicant, Organization as org, Recruiter, Job, Application, Interview

admin.site.register(User)
admin.site.register(Exp)
admin.site.register(Edu)
admin.site.register(Skill)
admin.site.register(Applicant)
admin.site.register(org)
admin.site.register(Recruiter)
admin.site.register(Job)
admin.site.register(Application)
admin.site.register(Interview)

# Register your models here.
