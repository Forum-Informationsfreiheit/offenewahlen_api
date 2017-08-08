from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name='viz'),
	url(r'^viz/', views.viz, name='viz'),
	url(r'^computing/', views.computing, name='computing'),
	url(r'^waiting/', views.waiting, name='waiting'),
	url(r'^test/', views.test, name='test'),
]