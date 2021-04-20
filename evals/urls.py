from django.urls import path
from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r"^accounts/", include("django.contrib.auth.urls")),
    path('accounts/new/<str:email>/', views.createAccount, name='createAccount'),
    path('accounts/newCreate', views.createAccountPost, name='createAccountPost'),
    path('accounts/new/', views.createAccountEmail, name='createAccountEmail'),
    path('accounts/exists/', views.accountExists, name='accountExists'),
    path('accounts/notFound/', views.accountNotFound, name='accountNotFound'),
    path('home/', views.home, name='home'),
    path('professor/', views.profHome, name='professor'),
    path('student/', views.stuHome, name='stuHome'),
    path('admin/', views.adminHome, name='adminHome'),
    path('groups/add/', views.addGroup, name='addGroup'),
    path('groups/add/submit', views.addGroupSubmit, name='addGroupSubmit'),
    path('groups/', views.groups, name='groups'),
    path('evals/assign', views.assignEval, name='assignEval'),
    path('evals/success', views.evalSuccess, name='evalSuccess'),
    path('evals/complete/<int:groupId>/', views.evalFillOut, name='evalFillOut'),
    path('students/' , views.students, name='students'),
    path('professor/visualizations/', views.visual, name='profVisual'),
    path('student/visualizations/', views.stuVisualizations, name='stuVisual'),
    path('courses/add/', views.addCourse, name='addCourse'),
    path('courses/', views.courses, name='courses'),
    path('notImplemented/', views.notImplemented, name='notImplemented'),
    path('', views.index, name='index'),
    
]