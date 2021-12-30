from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom User
class User(AbstractUser):
	username = models.CharField(unique=True,max_length=20)
	email = models.EmailField(unique=True)
	
	first_name = models.CharField(max_length=10)
	last_name = models.CharField(max_length=10)
	date_of_birth = models.DateField()

	
	is_official = models.BooleanField(default=False)
	is_teacher = models.BooleanField(default=False)
	is_student = models.BooleanField(default=False)


	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username','first_name','last_name','date_of_birth']


# Extra data for students
class StudentProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	father_name = models.CharField(max_length=10)
	mother_name = models.CharField(max_length=10)

	def __str__(self):
		return str(self.user) +" student profile"


# Extra data just for teacher
class TeacherProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	degree = models.CharField(max_length=10)

	def __str__(self):
		return str(self.user) +" teacher profile"


# passcode for registering teacher
class TeacherCode(models.Model):
	code = models.CharField(max_length=10)

	def __str__(self):
		return "Code "+ str(self.id)