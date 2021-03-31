from .models import AssessmentAssigned, AssessmentSubmitted, Score, Category, Student, Group
from datetime import datetime
import pytz

class service:
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