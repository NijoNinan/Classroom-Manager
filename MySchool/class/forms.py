from django import forms
from .models import *
from django.core.validators import MinLengthValidator

class NewClassForm(forms.ModelForm):
	class Meta:
		model = Classes
		fields = [
			'name',
			'info',
		]

class JoinClassForm(forms.Form):
	code = forms.CharField(
		max_length = 7,
		validators= [MinLengthValidator(7,"The Code is 7 characters")]
	)

class NewContent(forms.ModelForm):
	share_notes = forms.FileField(
		widget = forms.ClearableFileInput(attrs={'multiple': True}),
		required = False
	)
	class Meta:
		model = Contents
		fields = [
			'title',
			'info',
		]