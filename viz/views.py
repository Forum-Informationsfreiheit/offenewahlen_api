from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
	return HttpResponse('Hier kommen die Visualisierungen.')

def stats(request):
	return HttpResponse('Hier kommen die Statistiken.')
