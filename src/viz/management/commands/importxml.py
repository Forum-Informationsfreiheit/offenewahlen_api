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
	def add_arguments(self, parser):
		parser.add_argument(
			'--local_path',
			dest='local_path',
			help='Specify a file path to import from',
		)

	def handle(self, *args, **options):
		if 'local_path' in options.keys():
			xml_data, xml_header = self.get_local_data(options['local_path'])
		else:
			xml_data, xml_header = self.get_network_data(options)

		self.write_raw_data_to_database(xml_data, xml_header)

		# check, if xml is already downloaded and imported via RawData-hashes
		# if not, convert xml to dict
		data = []
		root = ET.fromstring(xml_data)

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

		for mun in data:
			time_data = datetime.datetime.strptime(
					mun['timestamp'], "%Y-%m-%d %H:%M:%SZ")
			time_data = timezone.make_aware(
				time_data, timezone.get_current_timezone())
			result = MunicipalityResult(
				eligible_voters = mun['eligible_voters'],
				votes = mun['votes'],
				valid = mun['valid'],
				invalid = mun['invalid'],
				#spatial_id = mun['spatial_id'],
				ts_result = time_data,
				is_final = False
			)
			result.save()

	def write_raw_data_to_database(self, xml_data, xml_header):
		"""
		Write raw data into table.
		"""
		timestamp_now = timezone.now()

		raw = RawData(
			timestamp = timestamp_now,
			hash = hashlib.md5(xml_data.encode()),
			content = xml_data,
			header = xml_header,
			dataformat = 'xml')
		raw.save()

	def get_local_data(self, local_path):
		"""
		Get the data from a local directory.
		"""
		print("Importing data from: {}".format(local_path))
		with open(local_path) as test_data_file:
			test_data = test_data_file.read()

		return (test_data, '')


	def get_network_data(self, options):
		"""
		Get the data from a network location.
		"""
		import_url = self._get_input_url(options)

		if import_url == '':
			print('No import url supplied!')
			return ''

		# make http request
		r = requests.get(import_url)
		return (r.text, r.header)

	def _get_input_url(self, options):
		"""
		Gets the import path from the kwargs or the config.json
		"""
		import_url = ''

		if 'import_url' in options.keys():
			import_url = options['import_url']

		try:
			with open("config.json") as config_file:
				config = json.load(config_file)
				import_url = config['url_xml']
		except:
			print("Config file not found!")

		return import_url

