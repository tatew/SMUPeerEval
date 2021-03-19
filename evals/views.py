from django.shortcuts import render, redirect
from .models import Course, Professor, Student, Group, projectGroup
from django.contrib.auth.decorators import login_required, permission_required
from .forms import CourseForm, SignUpForm
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User, Permission
from datetime import datetime
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate


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
    courses = Course.objects.order_by('courseName')
    selected = courses[0].id
    
    if request.method == 'POST':
        print(request.POST)
        selected = int(request.POST['course'])
        

    students = students = Student.objects.filter(enrollment__course_id=selected)
    context = {
        'courses': courses,
        'selected': selected,
        'students': students
    }
    return render(request, 'evals/addGroup.html', context)

def addGroupSubmit(request):
    if request.method == 'POST':
        print(request.POST)
        group = Group(course_id=int(request.POST['courseId']), groupName=request.POST['groupName'])
        group.save()
        newGroup = Group.objects.latest('id')

        for studentId in request.POST.getlist('students'):
            stuId = int(studentId)
            student = Student.objects.get(id=stuId)
            pGroup = projectGroup(student=student, group=newGroup)
            pGroup.save()
        

    return HttpResponseRedirect('/')

@permission_required('evals.is_professor')
def assignEval(request):

    if request.method == 'POST':
        print(request.POST)
        return HttpResponseRedirect('success')

    courses = Course.objects.order_by('courseName')
    now = datetime.now()
    date = now.strftime("%B %d %Y %H:%M:%S")
    context = {
        'date': date,
        'courses': courses
    }

    return render(request, 'evals/assignEval.html', context)

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
    courses = Course.objects.order_by('courseName')
    groups = Group.objects.order_by('groupName')
    students = []
    selected = -1
    groupName = ""
    groupCourseName = ""

    if request.method =='POST':
        print(request.POST)
        if 'course' in request.POST:
            if (request.POST['course'] == '-1'):
                courses = Course.objects.order_by('courseName')
            else:
                groups = Group.objects.filter(course__id=request.POST['course'])
                selected = int(request.POST['course'])
        if 'groupId' in request.POST:
            students = Student.objects.filter(projectgroup__group_id=int(request.POST['groupId']))
            groupName = Group.objects.get(id=int(request.POST['groupId'])).groupName
            groupCourseName = Group.objects.get(id=int(request.POST['groupId'])).course.courseName

    
    context = {
        'courses': courses,
        'selected': selected,
        'groups': groups,
        'students': students,
        'groupName': groupName,
        'groupCourseName': groupCourseName
    }

    return render(request, 'evals/groups.html', context)

@permission_required('evals.is_professor')
def visual(request):
    return render(request, 'evals/visualizations.html')

def createAccountEmail(request):
    if request.method == 'POST':
        email = request.POST['email']
        return HttpResponseRedirect(f'/accounts/new/{email}/')
    else:
        return render(request, 'evals/createAccountEmail.html')

def createAccountPost(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            permission = Permission.objects.get(codename='is_professor')
            user.user_permissions.add(permission)
            login(request, user)
            return HttpResponseRedirect('../../dashboard/')

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
        form = UserCreationForm()
        context = {
            'email': email,
            'form': form
        }
        
        return render(request, 'evals/newAccount.html', context)
    else:
        return HttpResponse("Account creation forbiden: Error Code 21-315")

def notImplemented(request):
    return HttpResponse("This link is not yet implemented. One of these days Tate will get his act together and get it done.")

@permission_required('evals.is_professor')
def evalSuccess(request):
    return render(request, 'evals/evalSuccess.html')