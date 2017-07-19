from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.

def waiting(request):
	template = loader.get_template('viz/waiting.html')
	return render(request, 'viz/waiting.html')

