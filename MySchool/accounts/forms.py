from django import forms
from Users.models import *
from django.contrib.auth.forms import UserCreationForm , UserChangeForm


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


class EditProfileForm(UserChangeForm):
	password = None
	current_password = forms.CharField(required=True, widget=forms.PasswordInput, label="Current password")

	class Meta:
		model = User
		fields = ['username','email','first_name','last_name','date_of_birth', 'current_password']

	def clean_current_password(self):
         valid = self.instance.check_password(self.cleaned_data['current_password'])
         if not valid:
             raise forms.ValidationError("Password is incorrect.")
         return valid