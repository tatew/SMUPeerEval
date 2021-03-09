from django.shortcuts import render, redirect
from .models import Course
from django.contrib.auth.decorators import login_required, permission_required


def index(request):
    if request.user.is_authenticated:
        return redirect('/dashboard')
    else:
        return render(request, 'evals/index.html')

@login_required
def dashboard(request):
    view_course = request.user.has_perm('evals.view_course')
    context = {
        'view_course': view_course
    }
    return render(request, 'evals/dashboard.html', context)

@permission_required('evals.view_course')
def courses(request):
    num_courses = Course.objects.count
    context = {
        'num_courses': num_courses
    }
    return render(request, 'evals/courses.html', context)