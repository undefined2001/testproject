from .models import Request
from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Student, Staff, Faculty, Announcement, Complain, Course, Course_Content, Request
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .forms import *


def index(request):
    return render(request, 'index.html')


def studentLogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if not user:
            messages.info(request, 'Invalid Credentials')
            return redirect('studentLogin')
        else:
            student = Student.objects.get(user=user)
            if user and student:
                if student.is_approved:
                    auth.login(request, user)
                    return redirect(studentProfile)
                else:
                    messages.info(request, "Wait For Approval")
    return render(request, 'student_login.html')


def facultyLogin(request):
    if request.method == 'POST':
        user_name = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=user_name, password=password)

        if user is not None and Faculty.objects.filter(user=user).exists():
            auth.login(request, user)
            return redirect('faculty_profile')

        else:
            messages.info(request, 'Invalid Credentials')
            # return redirect('facultyLogin')
            # return HttpResponse("Faculty")
    return render(request, 'faculty_login.html')


def staffLogin(request):
    if request.method == 'POST':
        user_name = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=user_name, password=password)

        if user is not None and Staff.objects.filter(user=user).exists():
            auth.login(request, user)
            return redirect('staffProfile')
            # return HttpResponse("staff")
        else:
            messages.info(request, 'Invalid Credentials')
            return redirect('staffLogin')

    return render(request, 'staff_login.html')


def studentRegister(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = (first_name + last_name).lower()
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Username Taken')
                return redirect('studentRegister')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('studentRegister')
            else:
                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.save()

                student = Student.objects.create(
                    user=user, email=email, first_name=first_name, last_name=last_name)
                student.save()
                return redirect('studentLogin')
        else:
            messages.info(request, 'Password not matching')
            return redirect('studentRegister')
    return render(request, 'student_reg.html')


# ========================================================================= profiles
@login_required(login_url='studentLogin')
def studentProfile(request):
    if Student.objects.filter(user=request.user).exists():
        user = request.user
        obj = User.objects.get(username=user)

        if Student.objects.filter(user=obj).exists():
            obj = Student.objects.get(user=obj)
            return render(request, 'student_profile.html', {'user': obj, "student": "student"})

        return render(request, 'student_profile.html', {'user': obj})
    else:
        return redirect('studentLogin')


@login_required(login_url='staffLogin')
def staffProfile(request):
    if Staff.objects.filter(user=request.user).exists():
        user = request.user
        obj = User.objects.get(username=user)
        if Staff.objects.filter(user=obj).exists():
            obj = Staff.objects.get(user=obj)
            return render(request, 'staff_profile.html', {'user': obj, "staff": "staff"})
        return render(request, 'staff_profile.html', {'user': obj})
    else:
        return redirect('staffLogin')


def faculty_profile(request):
    user = Faculty.objects.get(user=request.user)
    return render(request, 'faculty_profile.html', {'user': user})


###########################################################################################


@login_required(login_url='studentLogin')
def studentAnnouncementView(request):
    if Student.objects.filter(user=request.user).exists():
        obj = Announcement.objects.all()
        return render(request, 'student_announcement_view.html', {'obj': obj[::-1]})
    else:
        return redirect('studentLogin')


@login_required(login_url='staffLogin')
def staffAnnouncementView(request):
    if Staff.objects.filter(user=request.user).exists():
        obj = Announcement.objects.all()
        if request.method == 'POST':
            announcement_id = request.POST['aid']
            announcement = Announcement.objects.get(id=announcement_id)
            announcement.delete()

        return render(request, 'staff_announcement_view.html', {'obj': obj[::-1]})
    else:
        return redirect('staffLogin')


@login_required(login_url='staffLogin')
def postAnnouncement(request):
    if Staff.objects.filter(user=request.user).exists():
        cuser = Staff.objects.get(user=request.user)
        if request.method == 'POST':
            subject = request.POST['subject']
            source = request.POST['source']
            statement = request.POST['statement']
            announcement = Announcement.objects.create(
                subject=subject, source=source, statement=statement, datetime=datetime.now(), posted_by=cuser)
            announcement.save()
            return redirect('staffAnnouncementView')
        return render(request, 'post_announcement.html')
    else:
        return redirect('staffLogin')


'''
course_faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, null=True, blank=True)
course_id = models.CharField(max_length=100, default=uuid.uuid4, unique=True)
course_name = models.TextField(max_length=100, unique=True)
course_description = models.TextField(max_length=200, blank=True, null=True)
course_credit = models.IntegerField()
course_department = models.CharField(max_length=100, blank=True, null=True)
'''


# Adding course goes Here
def add_course(request):
    if request.method == "POST":
        faculty = Faculty.objects.get(user=request.user)
        course_id = request.POST['course_code']
        course_title = request.POST['course_title']
        course_desc = request.POST['course_desc']
        course_dep = request.POST['course_dep']
        course_credit = request.POST['course_credit']
        course = Course(course_faculty=faculty, course_id=course_id, course_name=course_title,
                        course_description=course_desc, course_department=course_dep,
                        course_credit=course_credit)
        course.save()
        return redirect('faculty_see_courses')
    return render(request, 'faculty_add_course.html')


def see_course_list(request):
    faculty = Faculty.objects.get(user=request.user)
    couses = Course.objects.filter(course_faculty=faculty)
    return render(request, "faculty_course_list.html", {'courses': couses})


def delete_course(request, id):
    course = Course.objects.get(id=id)
    print(course)
    course.delete()
    return redirect("faculty_see_courses")


def faculty_announcements(request):
    return render(request, "faculty_add_announcement.html")


def accept_student_request(request):
    pass


def announcement_for_students(request):
    pass


@login_required(login_url='studentLogin')
def complainStudentView(request):
    if Student.objects.filter(user=request.user).exists():
        user = request.user
        complain = Complain.objects.all()
        # n_complain = []
        # for c in complain:
        #     if c.posted_by == user:
        #         n_complain.append(c)
        # context = {
        #     'complain': n_complain[::-1]
        # }
        context = {
            'complain': complain[::-1]
        }
        return render(request, 'complain_student_view.html', context)
    else:
        return redirect('studentLogin')


@login_required(login_url='staffLogin')
def complainStaffView(request):
    if Staff.objects.filter(user=request.user).exists():
        cuser = Staff.objects.get(user=request.user)
        complain = Complain.objects.all()
        context = {
            'complain': complain[::-1]
        }
        if request.method == 'POST' and request.POST['status'] == 'resolved':
            cnum = request.POST['cnum']
            status = "resolved"
            resolved_by = cuser

            complain = Complain.objects.get(cnumber=cnum)
            complain.status = status
            complain.resolved_by = resolved_by
            complain.save()
            return redirect('complainStaffView')
        elif request.method == 'POST' and request.POST['status'] == 'rejected':
            cnum = request.POST['cnum']
            status = "rejected"
            resolved_by = cuser

            complain = Complain.objects.get(cnumber=cnum)
            complain.status = status
            complain.resolved_by = resolved_by
            complain.save()
            return redirect('complainStaffView')
        return render(request, 'complain_staff_view.html', context)
    else:
        return redirect('staffLogin')


@login_required(login_url='studentLogin')
def postComplain(request):
    if Student.objects.filter(user=request.user).exists():
        cuser = Student.objects.get(user=request.user)
        if request.method == 'POST':
            tag = request.POST['tag']
            statement = request.POST['statement']

            complain = Complain.objects.create(
                tag=tag, statement=statement, datetime=datetime.now(), posted_by=cuser)
            complain.save()
            return redirect('complainStudentView')
        return render(request, 'post_complain.html')
    else:
        return redirect('studentLogin')


@login_required(login_url='studentLogin')
def studentProfile(request):

    if Student.objects.filter(user=request.user).exists():
        user = request.user
        obj = User.objects.get(username=user)
        if Student.objects.filter(user=obj).exists():
            obj = Student.objects.get(user=obj)
            comp = Complain.objects.all()
            cont = Course_Content.objects.all()
            comp_count = 0
            res_count = 0
            post_count = 0
            for c in comp:
                if c.posted_by == obj:
                    comp_count += 1

                if c.status == "resolved":
                    res_count += 1
            for c in cont:
                if c.upload_by == obj:
                    post_count += 1
            return render(request, 'student_profile.html', {'user': obj, "student": "student", 'cc': comp_count, 'ccc': post_count, "rcc": res_count})

        return render(request, 'student_profile.html', {'user': obj, 'cc': comp_count, 'ccc': post_count, "rcc": res_count})
    else:
        return redirect('studentLogin')


# Painding Request View

def staff_pending_request_view(request):
    students = Student.objects.filter(is_approved=False)
    print(students)

    return render(request, 'staff_approve_student.html', {"students": students})


def approve_student(request, id):
    student = Student.objects.get(id=id)
    student.is_approved = True
    student.save()
    return redirect('approve_request_pending')


# Module 4 Goes Here
def add_faculty(request):
    form = FacultyCreationForm()
    if request.method == "POST":
        form = FacultyCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('staffProfile')
    return render(request, 'staff_add_faculty.html', {'form': form})


# Logout Views Goes Here
def student_logout(request):
    logout(request)
    return redirect('studentLogin')


def staff_logout(request):
    logout(request)
    return redirect('staffLogin')


# JAS Modifications.
def student_advising(request):
    courses = Course.objects.all()
    print(courses)
    return render(request, 'student_advising.html', {'courses': courses})


def make_request(request):
    if request.method == 'POST':
        course_id = request.POST.get('course_id')
        faculty_id = request.POST.get('faculty_id')

        if request.user.is_authenticated:
            current_student = Student.objects.get(user=request.user)

            course = Course.objects.get(id=course_id)
            faculty = Faculty.objects.get(id=faculty_id)

            if not Request.objects.filter(student=current_student, course=course, faculty=faculty).exists():
                new_request = Request(
                    student=current_student, course=course, faculty=faculty)
                new_request.save()

    return redirect('student_advising')


# def request_list(request):
#     current_teacher = request.user.faculty
#     teacher_requests = Request.objects.filter(faculty=current_teacher)
#     return render(request, 'request_list.html', {'teacher_requests': teacher_requests})


# def request_list(request):
#     if request.method == 'POST':
#         request_id = request.POST.get('request_id')
#         action = request.POST.get('action')

#         request_instance = get_object_or_404(Request, id=request_id)

#         if action == 'decline':
#             request_instance.status = False
#             request_instance.save()

#         # Need to add logic for Approve.

#     teacher_requests = Request.objects.filter(faculty=request.user.faculty)
#     return render(request, 'request_list.html', {'teacher_requests': teacher_requests})


def request_list(request):
    if request.method == 'POST':
        request_id = request.POST.get('request_id')
        action = request.POST.get('action')

        request_instance = get_object_or_404(Request, id=request_id)

        if action == 'approve':
            request_instance.is_approved = True

            # Create a new entry in the Enrolled model if not already approved
            if not Enrolled.objects.filter(student=request_instance.student, course=request_instance.course, approval=request_instance.faculty, is_approved=True).exists():
                enrolled_instance = Enrolled(
                    student=request_instance.student, course=request_instance.course, approval=request_instance.faculty, is_approved=True)
                enrolled_instance.save()

        elif action == 'decline':
            request_instance.is_approved = False

        request_instance.save()

    teacher_requests = Request.objects.filter(faculty=request.user.faculty)
    return render(request, 'request_list.html', {'teacher_requests': teacher_requests})
