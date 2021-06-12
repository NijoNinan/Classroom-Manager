from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

# Register the Custom User
admin.site.register(User, UserAdmin)
admin.site.register(StudentProfile)
admin.site.register(TeacherProfile)
admin.site.register(TeacherCode)