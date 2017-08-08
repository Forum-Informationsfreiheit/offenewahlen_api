from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

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
