from .models import AssessmentAssigned, AssessmentSubmitted, Score, Category, Student, Group, Professor
from django.contrib.auth.models import User, Permission
from datetime import datetime
import pytz

class service:

    def getUserType(email):
        isProf = True
        try:
            Professor.objects.get(email=email)
        except:
            isProf = False
        isStu = True
        try: 
            Student.objects.get(email=email)
        except:
            isStu = False

        if isStu:
            return 'student'
        elif isProf:
            return 'professor'
        else:
            return None

    def getFirstNameForEmail(email):
        userType = service.getUserType(email);
        if userType == 'professor':
            return Professor.objects.get(email=email).firstName
        if userType == 'student':
            return Student.objects.get(email=email).firstName

    def getLastNameForEmail(email):
        userType = service.getUserType(email);
        if userType == 'professor':
            return Professor.objects.get(email=email).lastName
        if userType == 'student':
            return Student.objects.get(email=email).lastName


    def assessmentCompleted(assessments):
        completed = True
        for assessment in assessments:
            if not AssessmentSubmitted.objects.filter(assessmentAssignedID=assessment.id).exists():
                completed = False
        return completed

    def recordScore(form, reviewer, group):
        assessment = AssessmentAssigned.objects.get(reviewer=reviewer, group=group, reviewee=form.get('reviewee'))
        assessmentSubmitted = AssessmentSubmitted(assessmentAssignedID=assessment, submitted=datetime.now(pytz.utc))
        assessmentSubmitted.save()
        for category in Category.objects.all():
            scoreValue = int(form.get(str(category.id)))
            score = Score(AssessmentSubmittedID=assessmentSubmitted, categoryID=category, score=scoreValue)
            score.save()