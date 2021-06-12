from django.urls import path
from .views import *


urlpatterns = [

	path('register/', Register.as_view(), name= 'register'),
	path('profile/', ViewProfile.as_view(), name= 'view_profile'),
]


	# path('editprofile/',views.EditProfile.as_view(), name= 'edit_profile'),