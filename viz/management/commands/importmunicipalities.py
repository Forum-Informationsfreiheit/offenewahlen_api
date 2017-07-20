from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from viz.models import Municipality
import json
import datetime

class Command(BaseCommand):

	def handle(self, *args, **options):
		# import 

		# convert to dict

		# check data

		# store data in database

		for mun in data:
			m = MunicipalityResult(
				spatial_id = mun[''],
				name = mun[''],
				district = mun[''],
				state = mun['']
			)
			m.save()

