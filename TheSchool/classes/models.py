from django.db import models
from Users.models import User

class Classes(models.Model):
	name = models.CharField(max_length=20)
	class_teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='class_teacher')
	info = models.TextField(blank=True)
	code = models.SlugField(unique=True, max_length=7)
	students = models.ManyToManyField(User)



	def __str__(self):
		return self.name +" ("+ self.code +")"

class Contents(models.Model):
	title = models.CharField(max_length=20)
	classes = models.ForeignKey(Classes, on_delete=models.CASCADE)
	info = models.TextField(blank=True)

	def __str__(self):
		return self.title +" ("+ str(self.classes.code) +")"	


# remember this
# it makes custom field for uploading
def getUploadDir(instance,filename):
	con = instance.contents.title
	classes = instance.contents.classes.code
	return "uploads/"+classes+"/"+con+"/"+filename

class ContentFiles(models.Model):
	contents = models.ForeignKey(Contents, on_delete=models.CASCADE)
	files = models.FileField(upload_to = getUploadDir)

	def __str__(self):
		l = str(self.files).split('/')
		return l[-1]

