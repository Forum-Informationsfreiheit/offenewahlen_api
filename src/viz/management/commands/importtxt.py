from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from viz.models import MunicipalityResult, RawData, PartyResult, RawData
import json
import requests
import datetime
import hashlib

class Command(BaseCommand):

	def handle(self, *args, **options):
		# make http request
		with open("config.json") as config_file:    
			config = json.load(config_file)

		r = requests.get(config['url_txt'])

		# check, if xml is already downloaded and imported via RawData-hashes
		
		# if not, convert txt to dict

		
		# check data => see importxml

		# store raw data in database => see importxml

