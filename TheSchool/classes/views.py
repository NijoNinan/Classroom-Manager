from django.shortcuts import render,redirect
from django.views import View
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import *
from django.urls import reverse_lazy


import string
import random


class AllClass(LoginRequiredMixin,View):
	template = 'classes/all.html'

	def get(self,request):
		context = dict()

		# if student show all the class enrolled
		if request.user.is_student:

			# classes = Classes.objects.filter(students=request.user) # same way for doing the below step
			classes = request.user.classes_set.all()
			
			context['classes'] = classes
			if len(context['classes']) == 0:
				messages.error(request,"You haven't enrolled in any Class !")

		# show all the classes that the teacher manages
		elif request.user.is_teacher:
			classes = Classes.objects.filter(class_teacher=request.user)
			context['classes'] = classes
			if len(context['classes']) == 0:
				messages.error(request,"You haven't created any Class !")

		# show all the classes in the database to admin
		else:
			classes = Classes.objects.all()
			context['classes'] = classes
			if len(context['classes']) == 0:
				messages.error(request,"There isn't any Class !")
		return render(request,self.template,context)


class CreateClass(LoginRequiredMixin, View):
	template = 'classes/create_class.html'

	def get(self,request):
		context = dict()

		# if not teacher error
		if not request.user.is_teacher:
			messages.error(request,"You don't have permission to add new Class !")
			return redirect(reverse_lazy('classes_all'))

		# if teacher then make a form
		form = NewClassForm()
		context['form'] = form
		return render(request, self.template, context)

	def post(self,request):
		if not request.user.is_teacher:
			messages.error(request,"You don't have permission to add new Class !")
			return redirect(reverse_lazy('classes_all'))
		

		context = dict()
		form = NewClassForm(request.POST)

		# if form is correct
		if form.is_valid():
			obj = form.save(commit=False)
			obj.class_teacher = request.user

			# generating code for class
			list_of_codes = Classes.objects.values_list('code', flat=True)
			obj.code = self.createRandomCode(list_of_codes)

			obj.save()

			messages.success(request,"Class created successfully !")
			return redirect(reverse_lazy('class_detail', args=[obj.code]))

		# if not filled properly
		context['form'] = form
		messages.error(request,"Error in filling the form !")
		return render(request, self.template, context)

	# function  for generating a unique code
	def createRandomCode(self, list_of_codes):
		code = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 7))
		if code in list_of_codes:
			return self.createRandomCode(list_of_codes)
		else:
			return code


class JoinClass(LoginRequiredMixin, View):
	template = 'classes/join_class.html'

	def get(self,request):
		if not request.user.is_student:
			messages.error(request,"You are not a student !")
			return redirect(reverse_lazy('classes_all'))

		context = dict()
		form = JoinClassForm()
		context["form"] = form
		return render(request, self.template, context)

	def post(self,request):
		if not request.user.is_student:
			messages.error(request,"You are not a student !")
			return redirect(reverse_lazy('classes_all'))

		form = JoinClassForm(request.POST)
		if form.is_valid():
			code = request.POST["code"]

			# checking if the code exists in db
			try:
				obj = Classes.objects.get(code=code)
				obj.students.add(request.user)
				messages.success(request,"You have enrolled to the class successfully !")
				return redirect(reverse_lazy('classes_all'))
			except:
				pass
				
		context = dict()
		context["form"] = form
		messages.error(request,"Please enter the correct Code !")
		return render(request, self.template, context)


class ViewClassDetail(LoginRequiredMixin, View):
	template = 'classes/class_detail.html'

	def get(self,request,code):
		try:
			obj = Classes.objects.get(code=code)
		except:
			messages.error(request,"The class code doesn't exists !")
			return redirect(reverse_lazy('classes_all'))

		context = dict()


		# requested by class teacher
		if request.user.is_teacher:
			if obj.class_teacher == request.user:
				contents = Contents.objects.filter(classes = obj)

				context["obj"] = obj
				context["contents"] = contents
				context["students"] = obj.students.all()

				return render(request, self.template , context)
			
			# not teacher's class
			else:
				messages.error(request,"You can't access that class !")
				return redirect(reverse_lazy('classes_all'))


		
		elif request.user.is_student:

			# class student
			if request.user in obj.students.all():
				contents = Contents.objects.filter(classes = obj)

				context["obj"] = obj
				context["contents"] = contents
				context["students"] = obj.students.all()

				return render(request, self.template , context)

			# not class student
			else:
				messages.error(request,"You can't access that class !")
				return redirect(reverse_lazy('classes_all'))

		# others
		else:
			messages.error(request,"You can't access that class !")
			return redirect(reverse_lazy('classes_all'))


class AddContents(LoginRequiredMixin, View):
	template = 'classes/add_contents.html'

	def get(self,request,code):
		try:
			obj = Classes.objects.get(code=code)
		except:
			messages.error(request,"The class code doesn't exists !")
			return redirect(reverse_lazy('classes_all'))

		context = dict()

		# if class teacher
		if request.user.is_teacher:
			if obj.class_teacher == request.user:
				form = NewContent()
				context["form"] = form
				context["code"] = code
				return render(request, self.template , context)
		else:
			messages.error(request,"You can't add contents to this class !")
			return redirect(reverse_lazy('classes_all'))


	def post(self,request,code):
		try:
			obj = Classes.objects.get(code=code)
		except:
			messages.error(request,"The class code doesn't exists !")
			return redirect(reverse_lazy('classes_all'))

		# if not correct teacher
		if not request.user.is_teacher or obj.class_teacher != request.user:
			messages.error(request,"You can't add contents to this class !")
			return redirect(reverse_lazy('classes_all'))

		form = NewContent(request.POST)

		# if correct
		if form.is_valid():
			con = form.save(commit=False)
			con.classes = obj
			con.save()

			files = request.FILES.getlist('share_notes')
			print(request.POST)
			print(files)
			for f in files:
				cf = ContentFiles.objects.create(contents = con, files = f)

			messages.success(request, con.title+" added to "+ obj.name+ " successfully !")
			return redirect(reverse_lazy('class_detail',args = [code,]))


		# if error
		messages.error(request,"Please fill in properly !")
		context = dict()
		context["form"] = form
		context["code"] = code

		return render(request, self.template , context)


class ViewContent(LoginRequiredMixin, View):
	template = 'classes/view_content.html'

	def get(self,request,code,cid):
		
		# if class exists
		try:
			classes = Classes.objects.get(code=code)
		except:
			messages.error(request,"The class doesn't exists !")
			return redirect(reverse_lazy('classes_all'))

		# if content exists
		try:
			content = Contents.objects.get(id=cid)
		except:
			messages.error(request,"The content doesn't exist !")
			return redirect(reverse_lazy('class_detail',args = [code,]))

		# if not teacher or student
		if not request.user.is_teacher and not request.user.is_student:
			messages.error(request,"You can't access contents of any class !")
			return redirect(reverse_lazy('classes_all'))

		# check if teacher but not class teacher and student but not of class
		if (request.user.is_teacher and classes.class_teacher != request.user) or (request.user.is_student and request.user not in classes.students.all()):
			messages.error(request,"You can't access contents of this class !")
			return redirect(reverse_lazy('classes_all'))

		uploads = ContentFiles.objects.filter(contents = content)

		context = {}
		context["code"] = code
		context["content"] = content
		context["uploads"] = uploads
		
		return render(request, self.template, context)



