from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.core import serializers
from viz.models import PollingStationResult, PartyResult, PollingStation, Election, Municipality, RegionalElectoralDistrict, District, State, Party, RawData
from django.http import JsonResponse
from django.core.cache import cache
from django.template.context_processors import csrf
from django.views.decorators.cache import cache_page
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

@cache_page(60 * 60) # 60mins
def api_result(request):
	data = {}

	psr_query = PollingStationResult.objects.select_related().all()
	for psr in psr_query: 
		gkz = str(psr.polling_station.municipality.kennzahl)
		data[gkz] = {}
		data[gkz]['gemeinde_name'] = psr.polling_station.municipality.name
		data[gkz]['gemeinde_code'] = psr.polling_station.municipality.code
		data[gkz]['eligible_voters'] = psr.eligible_voters
		data[gkz]['votes'] = psr.votes
		data[gkz]['valid'] = psr.valid
		data[gkz]['invalid'] = psr.invalid
		data[gkz]['ts'] = psr.ts_result
		data[gkz]['election'] = psr.election.short_name

		pr_query = psr.partyresult_set.select_related().all()
		for pr in pr_query:
			data[gkz][str(pr.party)] = pr.votes

	return JsonResponse(data, safe=False)

QUEUE_KEY = 'nrw13'

@cache_page(60 * 60) # 60mins
def api_result_nrw13(request):

	queue = cache.get(QUEUE_KEY)
	data = {}

	psr_query = PollingStationResult.objects.select_related().filter(election__short_name='nrw13').all()
	for psr in psr_query: 
		gkz = str(psr.polling_station.municipality.kennzahl)
		data[gkz] = {}
		data[gkz]['gemeinde_name'] = psr.polling_station.municipality.name
		data[gkz]['gemeinde_code'] = psr.polling_station.municipality.code
		data[gkz]['eligible_voters'] = psr.eligible_voters
		data[gkz]['votes'] = psr.votes
		data[gkz]['valid'] = psr.valid
		data[gkz]['invalid'] = psr.invalid
		data[gkz]['ts'] = psr.ts_result
		data[gkz]['election'] = psr.election.short_name

		pr_query = psr.partyresult_set.select_related().all()
		for pr in pr_query:
			data[gkz][str(pr.party)] = pr.votes

	return JsonResponse(data, safe=False)

# @cache_page(60 * 60) # 60mins
def api_result_nrw17(request):
	data = {}

	psr_query = PollingStationResult.objects.select_related().filter(election__short_name='nrw17').all()
	for psr in psr_query: 
		gkz = str(psr.polling_station.municipality.kennzahl)
		data[gkz] = {}
		data[gkz]['gemeinde_name'] = psr.polling_station.municipality.name
		data[gkz]['gemeinde_code'] = psr.polling_station.municipality.code
		data[gkz]['eligible_voters'] = psr.eligible_voters
		data[gkz]['votes'] = psr.votes
		data[gkz]['valid'] = psr.valid
		data[gkz]['invalid'] = psr.invalid
		data[gkz]['ts'] = psr.ts_result
		data[gkz]['election'] = psr.election.short_name

		pr_query = psr.partyresult_set.select_related().all()
		for pr in pr_query:
			data[gkz][str(pr.party)] = pr.votes

	return JsonResponse(data, safe=False)

def api_base_election(request):
	result = Election.objects.values()
	data = [entry for entry in result]

	return JsonResponse(data, safe=False)

def api_base_list(request):
	result = List.objects.values()
	data = [entry for entry in result]

	return JsonResponse(data, safe=False)

def api_base_municipality(request):
	result = Municipality.objects.values()
	data = [entry for entry in result]

	return JsonResponse(data, safe=False)

def api_base_pollingstation(request):
	result = PollingStation.objects.values()
	data = [entry for entry in result]

	return JsonResponse(data, safe=False)

def api_base_red(request):
	result = RegionalElectoralDistrict.objects.values()
	data = [entry for entry in result]

	return JsonResponse(data, safe=False)

def api_base_district(request):
	result = District.objects.values()
	data = [entry for entry in result]

	return JsonResponse(data, safe=False)

def api_base_state(request):
	result = State.objects.values()
	data = [entry for entry in result]

	return JsonResponse(data, safe=False)

def api_base_party(request):
	result = Party.objects.values()
	data = [entry for entry in result]

	return JsonResponse(data, safe=False)

def api_geom(request):

	with open('data/setup/municipalities_topojson_999_20170101.json') as data_file:
		data = data_file.read()
	geom_data = json.loads(data)

	return JsonResponse(geom_data, safe=False)

def api_rawdata(request):
	result = RawData.objects.values()
	rd_data = [entry for entry in result]

	return JsonResponse(rd_data, safe=False)


