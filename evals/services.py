from .models import AssessmentAssigned, AssessmentSubmitted

class service:
    def assessmentCompleted(assessments):
        completed = True
        for assessment in assessments:
            if not AssessmentSubmitted.objects.filter(assessmentAssignedID=assessment.id).exists():
                completed = False

        return completed
