from django.shortcuts import render
from .models import Course

def index(request):
    num_courses = Course.objects.count
    context = {
        'num_courses': num_courses
    }
    return render(request, 'evals/index.html', context)