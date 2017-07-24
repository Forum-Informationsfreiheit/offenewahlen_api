from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from viz.models import MunicipalityResult, RawData, PartyResult, Municipality, RawData
import json
import xml.etree.ElementTree as ET
import pprint
import requests
import datetime
import hashlib

class Command(BaseCommand):

	def handle(self, *args, **options):
		# make http request
		with open("config.json") as config_file:    
			config = json.load(config_file)

		r = requests.get(config['url_xml'])

		# check, if xml is already downloaded and imported via RawData-hashes
		
		# if not, convert xml to dict
		data = []
		root = ET.fromstring(r.text)

		for municipality in root.iter('municipality'):
			tmp = {}
			for elem in municipality:
				tmp.update({elem.tag: elem.text})
			data.append(tmp)

		# check data
		# is_wrong = False
		# for mun in data:
		# 	print(mun['spatial_id'])
		# 	party_sum = 0
		# 	for party in config['parties']:
		# 		party_sum += int(mun[party])
		# 	print(int(mun['valid']) == party_sum)
		# 	print(int(mun['votes']) == int(mun['valid']) + int(mun['invalid']))
		# 	print(int(mun['eligible_voters']) >= int(mun['valid']))

			# check if timestamp is between first closing of polling station and now.

		#print('all checks: '+str(is_wrong))
		# 2017-10-15 15:23:38Z

		timestamp_now = timezone.now()

		# store raw data in database
		raw = RawData(
				timestamp = timestamp_now,
				hash = hashlib.md5(r.text.encode()),
				content = r.text,
				header = r.headers,
				dataformat = 'xml'
			)
		raw.save()

		# store results in database
		for mun in data:
			result = MunicipalityResult(
				eligible_voters = mun['eligible_voters'],
				votes = mun['votes'],
				valid = mun['valid'],
				invalid = mun['invalid'],
				#spatial_id = mun['spatial_id'],
				ts_result = datetime.datetime.strptime(mun['timestamp'], "%Y-%m-%d %H:%M:%SZ"),
				is_final = False
			)
			result.save()

