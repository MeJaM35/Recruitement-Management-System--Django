from django.contrib import admin
from .models import User, Exp, Edu, Skill, Applicant

admin.site.register(User)
admin.site.register(Exp)
admin.site.register(Edu)
admin.site.register(Skill)
admin.site.register(Applicant)

# Register your models here.
