from django.shortcuts import render
from django.views import View
from .forms import *
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from Users.models import TeacherCode
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin



# Sign Up for User
class Register(View):
	template = "accounts/register.html"

	def get(self,request):
		# forms
		smainform = RegisterForm()
		tmainform = RegisterForm()
		sForm = StudentProfileForm()
		tForm = TeacherProfileForm()

		# context dic
		context = dict()
		context["smainform"] = smainform
		context["tmainform"] = tmainform
		context['sForm']=sForm
		context['tForm']=tForm

		return render(request, self.template, context)

	def post(self,request):
		# for student register
		if 'stud' in request.POST:
			return self.saveStudent(request)

		# for teacher registration
		elif 'teach' in request.POST:
			return self.saveTeacher(request)
		
		return redirect(reverse_lazy('register'))


	# function for saving the student
	def saveStudent(self,request):
		smainform = RegisterForm(request.POST)
		sForm = StudentProfileForm(request.POST)
		
		# if everything is proper
		if smainform.is_valid() and sForm.is_valid():

			u = smainform.save(commit=False)
			u.is_student = True
			u.save()
			
			prof = sForm.save(commit=False)
			prof.user = u
			prof.save()

			login(request,u)
			messages.success(request,'Student added successfully.')
			return redirect(reverse_lazy('view_profile'))


		# if anything wrong
		messages.error(request,'Fill in properly!')
		
		tmainform = RegisterForm()
		tForm = TeacherProfileForm()
		
		context = dict()
		context["smainform"] = smainform
		context["tmainform"] = tmainform
		context['sForm']=sForm
		context['tForm']=tForm
		
		return render(request, self.template, context)


	# function for saving the teacher
	def saveTeacher(self,request):
		tmainform = RegisterForm(request.POST)
		tForm = TeacherProfileForm(request.POST)
		
		# if everything is proper
		if tmainform.is_valid() and tForm.is_valid():

			# checking if the code is correct
			code = request.POST["code"]
			refCode = TeacherCode.objects.filter(code = code)
			if refCode.exists():
				refCode.delete()

				u = tmainform.save(commit=False)
				u.is_teacher = True
				u.save()
				
				prof = tForm.save(commit=False)
				prof.user = u
				prof.save()

				login(request,u)
				messages.success(request,'Teacher added successfully.')
				return redirect(reverse_lazy('view_profile'))
			
			else:
				messages.error(request,'Code is invalid')

		
		else:
			messages.error(request,'Fill in properly!')
		
		# if anything wrong
		smainform = RegisterForm()
		sForm = StudentProfileForm()
		
		context = dict()
		context["smainform"] = smainform
		context["tmainform"] = tmainform
		context['sForm']=sForm
		context['tForm']=tForm
		
		return render(request, self.template, context)


# view profile of the user
class ViewProfile(LoginRequiredMixin,View):
	def get(self,request):
		return render(request, "accounts/profile.html", {'user': request.user})