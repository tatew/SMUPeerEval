from django.shortcuts import render, redirect
from .models import Course
from django.contrib.auth.decorators import login_required


def index(request):
    if request.user.is_authenticated:
        return redirect('/dashboard')
    else:
        return render(request, 'evals/index.html')

@login_required
def dashboard(request):
    num_courses = Course.objects.count
    context = {
        'num_courses': num_courses
    }
    return render(request, 'evals/dashboard.html', context)