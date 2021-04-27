from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User, Permission
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import Q, Avg
from datetime import datetime
from .forms import CourseForm, SignUpForm
from .models import Course, Professor, Student, Group, projectGroup, AssessmentAssigned, Enrollment, AssessmentSubmitted, Category, Score
import pytz
from .services import service


def index(request):
    if request.user.is_authenticated:
        return redirect('/home')
    else:
        return render(request, 'evals/index.html')

@login_required
def home(request):
    is_prof = request.user.has_perm('evals.is_professor')
    if (is_prof):
        return redirect(profHome)
    is_student = request.user.has_perm('evals.is_student')
    if (is_student):
        return redirect(stuHome)
    is_admin = request.user.has_perm('evals.is_admin')
    if (is_admin):
        return redirect(adminHome)
        
@permission_required('evals.is_student')
def stuHome(request):
    student = Student.objects.get(email=request.user.email)
    assessments = AssessmentAssigned.objects.filter(reviewer=student.studentNumber)
    groupIds = assessments.values('group').distinct()

    groupObjs = []
    for groupId in groupIds:
        group = Group.objects.get(id=groupId['group'])
        assessmentsForGroup = assessments.filter(group=group.id)
        due = assessmentsForGroup[0].expiration
        groupObj = {
            'group': group,
            'submitted': service.assessmentCompleted(assessmentsForGroup),
            'due': due
        }
        groupObjs.append(groupObj)

    context = {
        'groups': groupObjs
    }
    return render(request, 'evals/stuHome.html', context)

@permission_required('evals.is_professor')
def profHome(request):
    return render(request, 'evals/profHome.html')


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
    selected = courses[0].CRN
    
    if request.method == 'POST':
        print(request.POST)
        selected = int(request.POST['course'])
        
    students = Student.objects.filter(enrollment__course_id=selected)
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
            student = Student.objects.get(studentNumber=stuId)
            pGroup = projectGroup(student=student, group=newGroup)
            pGroup.save()
        

    return HttpResponseRedirect('/')

@permission_required('evals.is_professor')
def assignEval(request):

    if request.method == 'POST':
        groups = Group.objects.filter(course=int(request.POST['course']))
        for group in groups:
            students = Student.objects.filter(projectgroup__group_id=group.id)
            for student in students:
                otherStudents = students.filter(~Q(studentNumber=student.studentNumber))
                for otherStudent in otherStudents:
                    date = datetime.strptime(request.POST['expire'], '%Y-%m-%d')
                    assessment = AssessmentAssigned(assigned=datetime.now(pytz.utc), reviewer=student, reviewee=otherStudent, group=group, expiration=date, message=request.POST['message'])
                    assessment.save()


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

        if (request.POST['stuName'] != ''):
            students = students.filter(lastName__icontains=request.POST['stuName'])

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
                groups = Group.objects.filter(course__CRN=request.POST['course'])
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
        email = request.POST['email'].lower()
        return HttpResponseRedirect(f'/accounts/new/{email}/')
    else:
        return render(request, 'evals/createAccountEmail.html')

def createAccount(request, email):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            userEmail = email
            user = authenticate(username=username, password=raw_password)
            user.email = userEmail
            user.first_name = service.getFirstNameForEmail(userEmail)
            user.last_name = service.getLastNameForEmail(userEmail)
            user.save()

            userType = service.getUserType(userEmail)
            if (userType == 'professor'):
                permission = Permission.objects.get(codename='is_professor')
                user.user_permissions.add(permission)

            if (userType == 'student'):
                permission = Permission.objects.get(codename='is_student')
                user.user_permissions.add(permission)

            if (userType == 'admin'):
                permission = Permission.objects.get(codename='is_admin')
                user.user_permissions.add(permission)

            login(request, user)
            return redirect('home')
        else:
            context = {
                'email': email,
                'form': form
            }
            return render(request, 'evals/newAccount.html', context)

    exists = True
    try:
        user = User.objects.get(email=email)
    except:
        exists = False

    if exists:
        return redirect('accountExists')

    userType = service.getUserType(email)
    print(exists, userType)
    if not exists and userType != None:
        form = UserCreationForm()
        context = {
            'email': email,
            'form': form
        }
        return render(request, 'evals/newAccount.html', context)
    else:
        return redirect('accountNotFound')

def accountExists(request):
    return render(request, 'evals/accountExists.html')

def accountNotFound(request):
    return render(request, 'evals/accountNotFound.html')

def notImplemented(request):
    return HttpResponse("This link is not yet implemented. One of these days Tate will get his act together and get it done.")

@permission_required('evals.is_professor')
def evalSuccess(request):
    return render(request, 'evals/evalSuccess.html')

@permission_required('evals.is_student')
def evalFillOut(request, groupId):
    reviewerStudent = Student.objects.get(email=request.user.email)
    group = Group.objects.get(id=groupId)
    reviewee = None
    if request.method == 'POST':
        print(request.POST)
        completed = request.POST.get('completed', False)
        if (completed):
            service.recordScore(request.POST, reviewerStudent, group)
        else:
            reviewee = Student.objects.get(studentNumber=request.POST['studentId'])

    students = Student.objects.filter(projectgroup__group_id=groupId).exclude(studentNumber=reviewerStudent.studentNumber)
    studentObjs = []
    assessments = []
    for stu in students:
        assessment = AssessmentAssigned.objects.get(reviewee=stu.studentNumber, reviewer=reviewerStudent.studentNumber, group=group.id)
        submitted = AssessmentSubmitted.objects.filter(assessmentAssignedID=assessment.id).exists()
        stuObj = {
            'student': stu,
            'submitted': submitted
        }
        studentObjs.append(stuObj)
        assessments.append(assessment)
        
    categories = Category.objects.all()


    context = {
        'group': group,
        'students': studentObjs,
        'course': group.course,
        'reviewee': reviewee,
        'categories': categories,
        'complete': service.assessmentCompleted(assessments)
    }
    return render(request, 'evals/eval.html', context)

@permission_required('evals.is_student')
def stuVisualizations(request):
    student = Student.objects.get(email=request.user.email)

    courses = Course.objects.filter(enrollment__student_id=student.studentNumber)
    course = courses.first()
    categories = Category.objects.all()

    if request.method == 'POST':
        course = courses.get(CRN=int(request.POST.get('course')))

    group = Group.objects.filter(projectgroup__student_id=student.studentNumber, projectgroup__group__course_id=course.CRN).first()
    print(group)
    scoresForCourse = Score.objects.filter(AssessmentSubmittedID__assessmentAssignedID__reviewee_id=student.studentNumber, AssessmentSubmittedID__assessmentAssignedID__group__course_id=course.CRN, categoryID__description='Overall')
    avgStu = scoresForCourse.aggregate(Avg('score'))['score__avg']
    if avgStu != None:
        avgStu = round(avgStu, 2)

    try:
        scoresForTeam = Score.objects.filter(AssessmentSubmittedID__assessmentAssignedID__group__course_id=course.CRN, AssessmentSubmittedID__assessmentAssignedID__group_id=group.id, categoryID__description='Overall')
        avgTeam = scoresForTeam.aggregate(Avg('score'))['score__avg']
        avgTeam = round(avgTeam, 2)
    except:
        avgTeam = None

    context = {
        'categories': categories,
        'courses': courses,
        'selected': course,
        'avgStu': avgStu,
        'avgTeam': avgTeam
    }
    return render(request, 'evals/stuVisualizations.html', context)

@permission_required('evals.is_admin')
def adminHome(request):
    return render(request, 'evals/adminHome.html')