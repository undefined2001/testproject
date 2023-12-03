from django.urls import path
from . import views


urlpatterns = [
    path('', views.studentLogin, name='studentLogin'),
    path('index/', views.index, name='index'),
    path('student-login/', views.studentLogin, name='studentLogin'),
    path('student-logout/', views.student_logout, name="student_logout"),
    path('faculty-login/', views.facultyLogin, name='facultyLogin'),
    path('staff-login/', views.staffLogin, name='staffLogin'),
    path('staff-logout/', views.staff_logout, name="staff_logout"),
    path('student-register/', views.studentRegister, name='studentRegister'),
    path('student-profile/', views.studentProfile, name='studentProfile'),
    path('faculty-profile/', views.faculty_profile, name='faculty_profile'),
    path('staff-profile/', views.staffProfile, name='staffProfile'),
    path('faculty-add-course/', views.add_course, name="faculty_add_course"),
    path('faculty-see-courses', views.see_course_list, name='faculty_see_courses'),
    path('faculty-delete-course/<int:id>', views.delete_course, name="faculty_delete_course"),
    path('faculty-make-announcement', views.faculty_announcements, name="faculty_make_announcement"),

    path('student-announcement-view/', views.studentAnnouncementView, name='studentAnnouncementView'),
    path('staff-announcement-view/', views.staffAnnouncementView, name='staffAnnouncementView'),
    path('post-announcement/', views.postAnnouncement, name='postAnnouncement'),

    path('complain-student-view/', views.complainStudentView, name='complainStudentView'),
    path('complain-staff-view/', views.complainStaffView, name='complainStaffView'),
    path('post-complain/', views.postComplain, name='postComplain'),


    #---------------------------------------------------#
    path('approval-staff-view/', views.staff_pending_request_view, name="approve_request_pending"),
    path('approve-student/<int:id>', views.approve_student, name="approve_request_confirmation"),

    #-----------------Module 4-----------------------#
    path('staff-add-faculty/', views.add_faculty, name='staff_add_faculty'),

]