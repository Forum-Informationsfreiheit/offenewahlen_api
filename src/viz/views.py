from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.core import serializers
from viz.models import PollingStationResult, ListResult, PollingStation, Election, Municipality, RegionalElectoralDistrict, District, State, Party, RawData, List
from django.http import JsonResponse
from django.core.cache import cache
from django.template.context_processors import csrf
from django.views.decorators.cache import cache_page
import json
import csv

def export_csv(filename, data):
	counter = 1
	with open(filename, 'w') as csvfile:
		csvwriter = csv.writer(csvfile, delimiter=',',quotechar='"')
		csvwriter.writerow(['id','gemeinde_name','gemeinde_kennzahl','gemeinde_code','eligible_voters','votes','valid','invalid','ts','spoe_nrw13','oevp_nrw13','fpoe_nrw13','gruene_nrw13','bzoe_nrw13','neos_nrw13','stronach_nrw13','wandel_nrw13','pirat_nrw13','kpoe_nrw13','slp_nrw13','euaus_nrw13','cpoe_nrw13'])

		for key, value in data.items():
			csvwriter.writerow([str(counter),str(value['gemeinde_name']),str(value['gemeinde_kennzahl']),str(value['gemeinde_code']),str(value['eligible_voters']),str(value['votes']),str(value['valid']),str(value['invalid']),str(value['ts']),str(value['spoe_nrw13']),str(value['oevp_nrw13']),str(value['fpoe_nrw13']),str(value['gruene_nrw13']),str(value['bzoe_nrw13']),str(value['neos_nrw13']),str(value['stronach_nrw13']),str(value['wandel_nrw13']),str(value['pirat_nrw13']),str(value['kpoe_nrw13']),str(value['slp_nrw13']),str(value['euaus_nrw13']),str(value['cpoe_nrw13'])])
			counter +=1

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

	return render(request, 'viz/index_viz.dtl')

@cache_page(60 * 60) # 60mins
def api_result_nrw13(request):

	data = {}
	elec_short = 'nrw13'
	#psr_query = PollingStationResult.objects.filter(election__short_name=elec_short).select_related('polling_station', 'polling_station__municipality')
	psr_query = PollingStationResult.objects.filter(election__short_name=elec_short).select_related('polling_station') 
	#lr_query = ListResult.objects.select_related('election_list', 'polling_station_result', 'polling_station_result__polling_station', 'polling_station_result__polling_station__municipality').filter(polling_station_result__election__short_name=elec_short)

	for psr in psr_query: 
		code = str(psr.polling_station.municipality.code)
		data[code] = {}
		data[code]['gemeinde_name'] = psr.polling_station.municipality.name
		data[code]['gemeinde_kennzahl'] = str(psr.polling_station.municipality.kennzahl)
		data[code]['gemeinde_code'] = code
		data[code]['eligible_voters'] = psr.eligible_voters
		data[code]['votes'] = psr.votes
		data[code]['valid'] = psr.valid
		data[code]['invalid'] = psr.invalid
		data[code]['ts'] = psr.ts_result

		lr_query = psr.listresult_set.all()
		for lr in lr_query:
			data[code][str(lr.election_list.short_name)] = lr.votes

	#export_csv('data/export/nrw13.csv', data)
	
	return JsonResponse(data, safe=False)

@cache_page(60 * 60) # 60mins
def api_result_nrw17(request):
	
	data = {}
	elec_short = 'nrw17'
	#psr_query = PollingStationResult.objects.filter(election__short_name=elec_short).select_related('polling_station', 'polling_station__municipality')
	psr_query = PollingStationResult.objects.filter(election__short_name=elec_short).select_related('polling_station') 
	#lr_query = ListResult.objects.select_related('election_list', 'polling_station_result', 'polling_station_result__polling_station', 'polling_station_result__polling_station__municipality').filter(polling_station_result__election__short_name=elec_short)

	for psr in psr_query: 
		code = str(psr.polling_station.municipality.code)
		data[code] = {}
		data[code]['gemeinde_name'] = psr.polling_station.municipality.name
		data[code]['gemeinde_kennzahl'] = str(psr.polling_station.municipality.kennzahl)
		data[code]['gemeinde_code'] = code
		data[code]['eligible_voters'] = psr.eligible_voters
		data[code]['votes'] = psr.votes
		data[code]['valid'] = psr.valid
		data[code]['invalid'] = psr.invalid
		data[code]['ts'] = psr.ts_result

		lr_query = psr.listresult_set.all()
		for lr in lr_query:
			data[code][lr.election_list.short_name] = lr.votes

	return JsonResponse(data, safe=False)

def api_base_election(request):
	result = Election.objects.values()
	data = {}
	for elec in result:
		data[elec['short_name']] = {}
		for key, value in elec.items():
			data[elec['short_name']][key] = value

	return JsonResponse(data, safe=False)

def api_base_list(request):
	result = List.objects.values()
	data = {}
	for lst in result:
		data[lst['short_name']] = {}
		for key, value in lst.items():
			data[lst['short_name']][key] = value

	return JsonResponse(data, safe=False)

def api_base_municipality(request):
	result = Municipality.objects.values()
	data = {}
	for mun in result:
		data[mun['code']] = {}
		for key, value in mun.items():
			data[mun['code']][key] = value

	return JsonResponse(data, safe=False)

def api_base_pollingstation(request):
	result = PollingStation.objects.values()
	data = {}
	#for ps in result:
	#	data[ps['municipality']['code']] = {}
	#	for key, value in ps.items():
	#		data[ps['municipality']['code']][key] = value
	data = [entry for entry in result]
	return JsonResponse(data, safe=False)

def api_base_red(request):
	result = RegionalElectoralDistrict.objects.values()
	data = {}
	for red in result:
		data[red['short_code']] = {}
		for key, value in red.items():
			data[red['short_code']][key] = value

	return JsonResponse(data, safe=False)

def api_base_district(request):
	result = District.objects.values()
	data = {}
	for district in result:
		data[district['short_code']] = {}
		for key, value in district.items():
			data[district['short_code']][key] = value

	return JsonResponse(data, safe=False)

def api_base_state(request):
	result = State.objects.values()
	data = {}
	for state in result:
		data[state['short_code']] = {}
		for key, value in state.items():
			data[state['short_code']][key] = value

	return JsonResponse(data, safe=False)

def api_base_party(request):
	result = Party.objects.values()
	data = {}
	for party in result:
		data[party['short_name']] = {}
		for key, value in party.items():
			data[party['short_name']][key] = value

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


