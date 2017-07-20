from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from viz.models import MunicipalityResult, RawData, PartyResult
import json
import requests
import datetime
import hashlib

class Command(BaseCommand):

	def handle(self, *args, **options):
		# import json


		# convert json to dict

		
		# check data => see importxml

		# store raw data in database => see importxml

