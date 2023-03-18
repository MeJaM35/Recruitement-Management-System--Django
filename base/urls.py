from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('register', views.register, name='register'),
    path('logout', views.logoutUser, name='logout'),
    path('login', views.loginUser, name='login'),


    path('applicant/more-details', views.applicant_edit, name='applicant-edit'),
    path('applicant/more-details/add-skill', views.add_skills, name='add-skill'),
    path('applicant/more-details/add-education', views.add_edu, name='add-edu'),
    path('applicant/more-details/add-experience', views.add_exp, name='add-exp'),
    path('applicant/edit-details/<str:pk>/', views.user_edit, name='user-edit'),
    path('applicant/view-profile', views.view_profile, name='view-profile'),

    path('organization/register', views.register_org, name='register-org'),
    path('organization/admin/register/<str:pk>', views.register_admin, name='register-admin'),
    path('organization/admin/add-recruiter/', views.add_recruiter, name='add-recruiter'),



    path('contact',views.contact, name='contact'),
   
    path('about', views.about, name='about'),

]