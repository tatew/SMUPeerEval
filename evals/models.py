from django.db import models

# Create your models here.
class Professor(models.Model):
    lastName = models.CharField(max_length=50)
    firstName = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    school = models.CharField(max_length=100)

class Course(models.Model):
    courseName = models.CharField(max_length=50)
    courseNumber = models.IntegerField()
    maxStudents = models.IntegerField()
    meetingTime = models.DateTimeField('meeting time')
    discipline = models.CharField(max_length=50)
    professor = models.ForeignKey(Professor, on_delete=models.RESTRICT)
