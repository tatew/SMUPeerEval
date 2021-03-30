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

class AssessmentAssigned(models.Model):
    reviewerID = models.ForeignKey(Student, on_delete=models.RESTRICT)
    revieweeID = models.ForeignKey(Student, on_delete=models.RESTRICT, related_name="AssessmentGrade")
    course = models.ForeignKey(Course, on_delete=models.RESTRICT)
    assigned = models.DateTimeField('Assigned:')
    expiration = models.DateField(null=True)
    message = models.TextField(default="")

class AssessmentSubmitted(models.Model):
    assessmentAssignedID = models.ForeignKey(AssessmentAssigned, on_delete=models.RESTRICT)
    submitted = models.DateTimeField('Submitted:')

class Category(models.Model):
    description = models.CharField(max_length=255)

class Score(models.Model):
    categoryID = models.ForeignKey(Category, on_delete=models.CASCADE)
    AssessmentSubmittedID = models.ForeignKey(AssessmentSubmitted, on_delete=models.RESTRICT)
    score = models.IntegerField()