from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from viz.models import Party
import json
import requests
import datetime
import hashlib

class Command(BaseCommand):

	def handle(self, *args, **options):
		# import 

		# convert to dict

		# check data

		# store data in database

		for party in data:
			p = Party(
				party_id = party[''],
				wikidata_id = party[''],
				name = party[''],
				short = party[''],
				family = party[''],
				description = party['']
			)
			p.save()

