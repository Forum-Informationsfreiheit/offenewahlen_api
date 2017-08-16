from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.core import serializers
from viz.models import PollingStationResult, PartyResult, PollingStation, Election, Municipality, RegionalElectoralDistrict, District, State, Party, RawData
from django.http import JsonResponse
import json

def index(request):
	return render(request, 'viz/index_viz.dtl')

def viz(request):
	return render(request, 'viz/index_viz.dtl')

def waiting(request):
	return render(request, 'viz/index_waiting.dtl')

def computing(request):
	return render(request, 'viz/index_computing.dtl')

def test(request):
	return render(request, 'viz/index_test.dtl')

def api(request):

	return render(request, 'viz/index_api.dtl')

def api_results(request):
	result = PollingStationResult.objects.values()
	psr_data = [entry for entry in result]
	result = PartyResult.objects.values()
	pr_data = [entry for entry in result]
	result = PollingStation.objects.values()
	ps_data = [entry for entry in result]

	return JsonResponse(psr_data, safe=False)

def api_basedata(request):
	result = Election.objects.values()
	e_data = [entry for entry in result]
	result = Municipality.objects.values()
	m_data = [entry for entry in result]
	result = RegionalElectoralDistrict.objects.values()
	red_data = [entry for entry in result]
	result = District.objects.values()
	d_data = [entry for entry in result]
	result = State.objects.values()
	s_data = [entry for entry in result]
	result = Party.objects.values()
	p_data = [entry for entry in result]

	return JsonResponse(e_data, safe=False)

def api_geom(request):

	with open('../data/setup/municipalities_topojson_999_20170101.json') as data_file:
		data = data_file.read()
	geom_data = json.loads(data)

	return JsonResponse(geom_data, safe=False)

def api_rawdata(request):
	result = RawData.objects.values()
	rd_data = [entry for entry in result]

	return JsonResponse(rd_data, safe=False)


