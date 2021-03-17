from django.urls import path
from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r"^accounts/", include("django.contrib.auth.urls")),
    path('accounts/new/<str:email>/', views.createAccount, name='createAccount'),
    path('accounts/new/', views.createAccountEmail, name='createAccountEmail'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('groups/add/', views.addGroup, name='addGroup'),
    path('groups/add/submit', views.addGroupSubmit, name='addGroupSubmit'),
    path('groups/', views.groups, name='groups'),
    path('evals/assign', views.assignEval, name='assignEval'),
    path('evals/success', views.evalSuccess, name='evalSuccess'),
    path('students/' , views.students, name='students'),
    path('visualizations/', views.visual, name='visual'),
    path('courses/add/', views.addCourse, name='addCourse'),
    path('courses/', views.courses, name='courses'),
    path('notImplemented/', views.notImplemented, name='notImplemented'),
    path('', views.index, name='index'),
    
]