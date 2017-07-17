from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.

def index(request):
	template = loader.get_template('viz/index.html')
	return render(request, 'viz/index.html')

def stats(request):
	template = loader.get_template('viz/stats.html')
	return render(request, 'viz/stats.html')
