from django.conf import settings
from django.core import serializers
from django.core.cache import cache
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.template import loader
from django.template.context_processors import csrf
from django.views.decorators.cache import cache_page
from viz.models import PollingStationResult, ListResult, PollingStation, Election, Municipality, RegionalElectoralDistrict, District, State, Party, RawData, List
from wsgiref.util import FileWrapper
import json
import csv
import os
import mimetypes

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

def viz_overview(request):
	return render(request, 'viz/index_viz_overview.dtl')

def viz_results_map(request):
	return render(request, 'viz/index_viz_result_map.dtl')

def viz_results_mapnrw13(request):
	return render(request, 'viz/index_viz_result_mapnrw13.dtl')

def viz_results_mapcanvas(request):
	return render(request, 'viz/index_viz_result_mapcanvas.dtl')

def viz_results_bar(request):
	return render(request, 'viz/index_viz_result_bar.dtl')

def viz_results_timeseries(request):
	return render(request, 'viz/index_viz_result_timeseries.dtl')

def serve_nrw13_csv(request):

	# Create the HttpResponse object with the appropriate CSV header.
	filename = 'data/export/nrw13.csv'
	wrapper = FileWrapper(open(filename))
	response = HttpResponse(wrapper, content_type = 'text/csv')
	response['Content-Length'] = os.path.getsize(filename)
	response['Content-Disposition'] = 'attachment; filename="nrw13.csv"'

	return response

def waiting(request):
	return render(request, 'viz/index_waiting.dtl')

def computing(request):
	return render(request, 'viz/index_computing.dtl')

def test(request):
	return render(request, 'viz/index_test.dtl')

@cache_page(60 * 60) # 60mins
def api_geom(request):

	with open('data/setup/municipalities_topojson_999_20170101.json') as data_file:
		data = data_file.read()
	geom_data = json.loads(data)

	return JsonResponse(geom_data, safe=False)
