from django.urls import path
from .views import *


urlpatterns = [
	path('',TeacherHome.as_view(), name='teacher_home'),
	path('create/',TeacherCreate.as_view(), name = 'teacher_create')

]