from django.conf.urls import url, include
# from rest_framework.routers import DefaultRouter
from . import views#, views_api

# router = DefaultRouter()
# router.register(r'election', views_api.ElectionInterface)
# router.register(r'district', views_api.DistrictInterface)
# router.register(r'municipality', views_api.MunicipalityInterface)
# router.register(r'party', views_api.PartyInterface)
# router.register(r'polling_station', views_api.PollingStationInterface)
# router.register(r'list', views_api.ListInterface)
# router.register(r'result', views_api.PollingStationResultInterface)
# router.register(r'regional_electoral_district',
# 	views_api.RegionalElectoralDistrictInterface)

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^loaderio-eac9628bcae9be5601e1f3c62594d162.txt$', views.load_test, name='load_test'),
	# url(r'^api/', include(router.urls)),
	# url(r'^api/geom/$', views.api_geom, name='api_geom'),
]
