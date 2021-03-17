from django.shortcuts import render, redirect
from .models import Course, Professor, Student
from django.contrib.auth.decorators import login_required, permission_required
from .forms import CourseForm
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User


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

@permission_required('evals.is_professor')
def addGroup(request):
    return render(request, 'evals/addGroup.html')

@permission_required('evals.is_professor')
def assignEval(request):
    return render(request, 'evals/assignEval.html')

@permission_required('evals.is_professor')
def students(request):
    courses = Course.objects.order_by('courseName')
    students = Student.objects.order_by('lastName')
    selected = -1
    lastName = 'checked'
    firstName = ''
    
    if request.method == 'POST':
        if request.POST['course'] != 'None':
            students = Student.objects.filter(enrollment__course_id=request.POST['course'])
            selected = int(request.POST['course'])
        
        if request.POST['sort'] == 'firstName':
            firstName = 'checked'
            lastName = ''

        students = students.order_by(request.POST['sort'])

    context = {
        'courses': courses,
        'students': students,
        'selected': selected,
        'firstName': firstName,
        'lastName': lastName
    }

    return render(request, 'evals/students.html', context)

@permission_required('evals.is_professor')
def groups(request):
    return render(request, 'evals/groups.html')

@permission_required('evals.is_professor')
def visual(request):
    return render(request, 'evals/visualizations.html')

def createAccountEmail(request):
    if request.method == 'POST':
        email = request.POST['email']
        return HttpResponseRedirect(f'/accounts/new/{email}/')
    else:
        return render(request, 'evals/createAccountEmail.html')

def createAccount(request, email):
    exists = True
    try:
        user = User.objects.get(email=email)
    except:
        exists = False
    isProf = True
    try:
        prof = Professor.objects.get(email=email)
    except:
        isProf = False

    print(exists, isProf)
    if not exists and isProf:
        if request.method =='POST':
            return HttpResponseRedirect('/index/')
        else:
            context = {
                'email': email
            }
            return render(request, 'evals/newAccount.html', context)
    else:
        return HttpResponse("Account creation forbiden: Error Code 21-315")

def notImplemented(request):
    return HttpResponse("This link is not yet implemented. One of these days Tate will get his act together and get it done.")