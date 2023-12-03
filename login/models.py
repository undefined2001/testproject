from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime

User = get_user_model()
# Create your models here.
class StudentAdmission(models.Model):
    admission_id = models.CharField(uuid.uuid4,max_length=10 ,unique=True)
    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=200, blank=True, null=True)
    applied_semester = models.CharField(max_length=200, blank=True, null=True)

class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=10 ,unique=True, null = True, blank=True)
    phone = models.CharField(max_length=200, blank=True, null=True)
    department = models.CharField(max_length=200, blank=True, null=True)
    enrolled_semester = models.CharField(max_length=200, blank=True, null=True)
    is_approved = models.BooleanField(default=False, null=True, blank=True)

    #Student_tutor = models.CharField(max_length=8, blank=True, null=True)
    def __str__(self):
        return self.student_id
    
class Faculty(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    faculty_initial = models.CharField(max_length=10, unique=True, blank=True, null=True)
    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=200, blank=True, null=True)
    department = models.CharField(max_length=200, blank=True, null=True)
    joined_date = models.DateField(default=datetime.now, blank=True)

    def __str__(self):
        return self.faculty_initial

class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=200, blank=True, null=True)
    joined_date = models.DateField(default=datetime.now, blank=True, null=True)
    def __str__(self):
        return self.first_name + " " + self.last_name

class StudentTutor(models.Model):
    pass


class Course(models.Model):
    course_faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, null=True, blank=True)
    course_id = models.CharField(max_length=10, null=True, blank=True)
    course_name = models.TextField(max_length=100, unique=True)
    course_description = models.TextField(max_length=200, blank=True, null=True)
    course_credit = models.IntegerField()
    course_department = models.CharField(max_length=100, blank=True, null=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    def __str__(self):
        return str(self.course_id)
    

class Enrolled(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)

class Announcement(models.Model):
    subject = models.CharField(max_length=100, blank=True, null=True)
    statement = models.TextField(max_length=1000, blank=True, null=True)
    datetime = models.DateTimeField(default=datetime.now, blank=True, null=True)
    source = models.CharField(max_length=100, blank=True, null=True)
    posted_by = models.ForeignKey(Staff, on_delete=models.CASCADE, blank=True, null=True)
    def __str__(self):
        return f"{self.posted_by} -> Announcement {self.subject}"

class CourseAnnouncement(models.Model):
    statement = models.TextField(max_length=1000, blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    posted_by = models.ForeignKey(Faculty, on_delete=models.CASCADE, blank=True, null=True)
    def __str__(self):
        return f"{self.posted_by} -> Announcement {self.anumber}"

class Complain(models.Model):
    cnumber = models.AutoField(primary_key=True)
    tag = models.CharField(max_length=100, blank=True, null=True)
    statement = models.TextField()
    datetime = models.DateTimeField(default=datetime.now, blank=True, null=True)
    posted_by = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="posted_by", blank=True, null=True)
    resolved_by = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name="resolved_by", blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True, default="pending")
    def __str__(self):
        return f"{self.posted_by} -> Complain {self.cnumber}"


class Course_Content(models.Model):
    course_content_id = models.CharField(max_length=100, default=uuid.uuid4, unique=True)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    course_content_tag = models.CharField(max_length=100, blank=True, null=True)
    course_content_description = models.CharField(max_length=5000, blank=True, null=True)
    #content_img = models.ImageField(upload_to='images/', blank=True, null=True)
    datetime = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    upload_by = models.ForeignKey(Student, on_delete=models.CASCADE)
    like = models.IntegerField(default=0)
    def __str__(self):
        return str(self.course_id)



class ClassRoutine(models.Model):
    DAYS_CHOICES = (
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    )

    time = models.TimeField()
    day = models.CharField(max_length=10, choices=DAYS_CHOICES)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    instructor = models.ForeignKey(Faculty, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.day} - {self.time} - {self.course}"