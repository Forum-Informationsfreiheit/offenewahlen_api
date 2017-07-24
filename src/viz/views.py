from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader


def index(request):
	return render(request, 'viz/index.dtl')

def stats(request):
	return render(request, 'viz/stats.dtl')
