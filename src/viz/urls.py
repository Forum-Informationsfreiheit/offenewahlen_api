from django.conf.urls import url
from . import views, views_api

app_name = 'viz'

urlpatterns = [
	url(r'^$', views.viz, name='viz'),
	url(r'^viz/$', views.viz_overview, name='viz_overview'),
	url(r'^viz/results-bar/$', views.viz_results_bar, name='viz_results_bar'),
	url(r'^viz/results-map/$', views.viz_results_map, name='viz_results_map'),
	url(r'^viz/results-mapnrw13/$', views.viz_results_mapnrw13, name='viz_results_mapnrw13'),
	url(r'^viz/results-mapcanvas/$', views.viz_results_mapcanvas, name='viz_results_mapcanvas'),
	url(r'^viz/results-timeseries', views.viz_results_timeseries, name='viz_results_timeseries'),
	url(r'^computing/', views.computing, name='computing'),
	url(r'^waiting/', views.waiting, name='waiting'),
	url(r'^test/', views.test, name='test'),
	url(r'^data/nrw13.csv$', views.serve_nrw13_csv, name='serve_nrw13_csv'),
	url(r'^api/$', views.api, name='api'),
	url(r'^api/election', views_api.ElectionInterface.as_view(), name='api_election'),
	url(r'^api/result/$', views.api_result, name='api_result'),
	url(r'^api/result/nrw13/$', views.api_result_nrw13, name='api_result_nrw13'),
	url(r'^api/result/nrw17/$', views.api_result_nrw17, name='api_result_nrw17'),
	url(r'^api/base/$', views.api_base_party, name='api_base_party'),
	url(r'^api/base/election/$', views.api_base_election, name='api_basedata_election'),
	url(r'^api/base/municipality/$', views.api_base_municipality, name='api_base_municipality'),
	url(r'^api/base/pollingstation/$', views.api_base_pollingstation, name='api_base_pollingstation'),
	url(r'^api/base/list/$', views.api_base_list, name='api_basedata_list'),
	url(r'^api/base/party/$', views.api_base_party, name='api_basedata_party'),
	url(r'^api/base/list/$', views.api_base_list, name='api_basedata_list'),
	url(r'^api/base/state/$', views.api_base_state, name='api_base_state'),
	url(r'^api/base/district/$', views.api_base_district, name='api_base_district'),
	url(r'^api/base/regionalelectoraldistrict/$', views.api_base_red, name='api_base_red'),
	url(r'^api/raw/$', views.api_rawdata, name='api_rawdata'),
	url(r'^api/geom/$', views.api_geom, name='api_geom'),
]
