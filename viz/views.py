from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
	return HttpResponse('Hello, world. Du bist auf der Website zur Nationalratswahl 2017.')
