import json
import csv
import os
from django.conf import settings
from django.core import serializers
from django.core.cache import cache
from django.http import HttpResponse, JsonResponse, FileResponse
from django.shortcuts import render
from django.template import loader
from django.template.context_processors import csrf
from django.views.decorators.cache import cache_page
from austria.models import PollingStationResult, ListResult, PollingStation, Election, Municipality, RegionalElectoralDistrict, District, State, Party, List
from wsgiref.util import FileWrapper


def index(request):
	return render(request, 'austria/index.dtl')

def load_test(request):
	# Create the HttpResponse object with the appropriate CSV header.
	filename = 'data/deployment/loaderio-eac9628bcae9be5601e1f3c62594d162.txt'
	wrapper = FileWrapper(open(filename))
	response = HttpResponse(wrapper, content_type = 'text/txt')
	response['Content-Length'] = os.path.getsize(filename)
	response['Content-Disposition'] = 'attachment; filename="loaderio-eac9628bcae9be5601e1f3c62594d162.txt"'

	return response
