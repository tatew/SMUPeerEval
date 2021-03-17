from django.db import models

# Create your models here.
class Professor(models.Model):
    lastName = models.CharField(max_length=50)
    firstName = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    school = models.CharField(max_length=100)
    class Meta:
        permissions = [
            ("is_professor", "If the User is a professor ")
        ]

class Course(models.Model):
    courseName = models.CharField(max_length=50)
    courseNumber = models.IntegerField()
    maxStudents = models.IntegerField()
    meetingTime = models.DateTimeField('meeting time')
    discipline = models.CharField(max_length=50)
    professor = models.ForeignKey(Professor, on_delete=models.RESTRICT)

class Student(models.Model):
    lastName = models.CharField(max_length=50)
    firstName = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    school = models.CharField(max_length=100)
    programme = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.firstName} {self.lastName}'

class Enrollment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.RESTRICT)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

class Group(models.Model):
    groupName = models.CharField(max_length=50)
    course = models.ForeignKey(Course, on_delete=models.RESTRICT)

class projectGroup(models.Model):
    group = models.ForeignKey(Group, on_delete=models.RESTRICT)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
