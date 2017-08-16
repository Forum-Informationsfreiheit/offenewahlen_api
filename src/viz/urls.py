from django.conf.urls import url
from . import views

app_name = 'viz'
urlpatterns = [
	url(r'^$', views.viz, name='viz'),
	url(r'^viz/', views.viz, name='viz'),
	url(r'^computing/', views.computing, name='computing'),
	url(r'^waiting/', views.waiting, name='waiting'),
	url(r'^test/', views.test, name='test'),
	url(r'^api/$', views.api, name='api'),
	url(r'^api/results/$', views.api_results, name='api_results'),
	url(r'^api/base/$', views.api_basedata, name='api_basedata'),
	url(r'^api/raw/$', views.api_rawdata, name='api_rawdata'),
	url(r'^api/geom/$', views.api_geom, name='api_geom'),
]