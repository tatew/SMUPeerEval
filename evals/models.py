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

    def __str__(self):
        return f'{self.discipline} {self.courseNumber} {self.courseName}'

class Student(models.Model):
    lastName = models.CharField(max_length=50)
    firstName = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    school = models.CharField(max_length=100)
    programme = models.CharField(max_length=100)

    class Meta:
        permissions = [
            ("is_student", "If the User is a Student ")
        ]

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

class peerAssessment(models.Model):
    reviewerID = models.ForeignKey(Student, on_delete=models.CASCADE)
    revieweeID = models.ForeignKey(Student, on_delete=models.CASCADE)
    assigned = meetingTime = models.DateTimeField('Assigned')
    submitted = meetingTime = models.DateTimeField('Submitted', default=None, blank=True, null=True)

class Score(models.Model):
    contribution1 = models.IntegerField()
    contribution2 = models.IntegerField()
    contribution3 = models.IntegerField()
    facilitation1 = models.IntegerField()
    facilitation2 = models.IntegerField()
    facilitation3 = models.IntegerField()
    planning1 = models.IntegerField()
    planning2 = models.IntegerField()
    planning3 = models.IntegerField()
    climate1 = models.IntegerField()
    climate2 = models.IntegerField()
    conflict1 = models.IntegerField()
    conflict2 = models.IntegerField()
    conflict3 = models.IntegerField()
    overall = models.IntegerField()



