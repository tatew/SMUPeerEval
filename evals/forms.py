from django.db import models
from .models import Course
from django.forms import ModelForm

class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = ['courseName', 'courseNumber', 'maxStudents', 'meetingTime', 'discipline', 'professor']