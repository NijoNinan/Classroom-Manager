from django.urls import path
from .views import *


urlpatterns = [

	path('', AllClass.as_view(), name= 'classes_all'),
	path('create/', CreateClass.as_view(), name= 'create_class'),
	path('join/', JoinClass.as_view(), name= 'join_class'),
	path('<slug:code>/', ViewClassDetail.as_view(), name= 'class_detail'),
	path('<slug:code>/addContent', AddContents.as_view(), name= 'class_add_content'),
	path('<slug:code>/<int:cid>', ViewContent.as_view(), name= 'class_view_content'),
]