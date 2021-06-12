from django import forms
from Users.models import *
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username','email','first_name','last_name','date_of_birth', "password1", "password2"]

class StudentProfileForm(forms.ModelForm):
	class Meta:
		model = StudentProfile

		fields = [
		"father_name",
		"mother_name",
		]

class TeacherProfileForm(forms.ModelForm):
	code = forms.CharField(max_length=7)
	class Meta:
		model = TeacherProfile
		fields = ['degree',]
