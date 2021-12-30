from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from Users.models import *
from django.http import HttpResponse

# python functions
import string
import random

class TeacherHome(LoginRequiredMixin,View):
	template = "teacher/home.html"
	def get(self,request):
		context = dict()

		if request.user.is_student:
			return render(request,self.template,context)
		elif request.user.is_teacher:
			return render(request,self.template,context)

		else:
			teacherList = User.objects.all().filter(is_teacher=True)
			context["teacherList"] = teacherList
			return render(request,self.template,context)



class TeacherCreate(LoginRequiredMixin,View):
	template = "teacher/code.html"
	def get(self,request):
		context = dict()

		if not request.user.is_student and not request.user.is_teacher:
			code = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 7))
			obj = TeacherCode.objects.create(code = code)
			context['code'] = code
			return render(request,self.template,context)
		else:
			return HttpResponse("Not Authorised!!!")
