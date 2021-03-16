from django.shortcuts import render, redirect
from .models import Course
from django.contrib.auth.decorators import login_required, permission_required
from .forms import CourseForm
from django.http import HttpResponseRedirect, HttpResponse


def index(request):
    if request.user.is_authenticated:
        return redirect('/dashboard')
    else:
        return render(request, 'evals/index.html')

@login_required
def dashboard(request):
    is_prof = request.user.has_perm('evals.is_professor')
    if is_prof :
        return render(request, 'evals/profHome.html')
    else:
        return render(request, 'evals/notFounnd.html')

@permission_required('evals.is_professor')
def courses(request):
    courses = Course.objects.order_by('courseNumber')
    context = {
        'courses': courses
    }
    return render(request, 'evals/courses.html', context)

def addCourse(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CourseForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            print(form.cleaned_data)
            course = Course(
                courseNumber=form.cleaned_data['courseNumber'], 
                courseName=form.cleaned_data['courseName'], 
                meetingTime=form.cleaned_data['meetingTime'], 
                maxStudents=form.cleaned_data['maxStudents'], 
                discipline=form.cleaned_data['discipline'], 
                professor=form.cleaned_data['professor']
            )
            course.save()
            return HttpResponseRedirect('/courses/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CourseForm()

    return render(request, 'evals/addCourse.html', {'form': form})

def notImplemented(request):
    return HttpResponse("This link is not yet implemented. One of these days Tate will get his act together and get it done.")