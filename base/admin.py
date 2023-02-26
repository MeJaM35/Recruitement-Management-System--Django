from django.contrib import admin
from .models import User, Exp, Edu, Skill, Applicant, Organization as org, Recruiter

admin.site.register(User)
admin.site.register(Exp)
admin.site.register(Edu)
admin.site.register(Skill)
admin.site.register(Applicant)
admin.site.register(org)
admin.site.register(Recruiter)

# Register your models here.
