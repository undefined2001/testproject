from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Student)
admin.site.register(Staff)
admin.site.register(Faculty)
admin.site.register(Course)
admin.site.register(Enrolled)
admin.site.register(Announcement)
admin.site.register(Request)
