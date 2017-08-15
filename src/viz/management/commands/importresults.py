from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from viz.models import MunicipalityResult, RawData, PartyResult, Municipality, RawData, Election, Party
import json
import xml.etree.ElementTree as ET
import pprint
import requests
import datetime
import hashlib

class Command(BaseCommand):

	help = 'Imports the election results'

	def add_arguments(self, parser):
		parser.add_argument(
			'file',
			nargs='?'
		)
		parser.add_argument(
			'election',
			default='nrw17',
			nargs='?'
		)
		parser.add_argument(
			'--location',
			dest='file_location',
			choices=['web', 'local'],
			default='none',
			help='Specify the location of the results file, either "web" or "local"'
		)
		parser.add_argument(
			'--mapping_file',
			dest='mapping_file',
			help='Specify a file path for the party mapping'
		)
		parser.add_argument(
			'--file_type',
			dest='file_type',
			choices=['xml', 'txt', 'json'],
			help='Specify the file type of results'
		)

	def handle(self, *args, **options):
		
		file_path = options['file']
		elec_short = options['election']
		election = Election.objects.get(short_name=elec_short)

		# get location where file is stored: web or local
		if options['file_location'] == 'none':
			if file_path[:4] == 'http' or file_path[:3] == 'ftp':
				location = 'web'
			else:
				location = 'local'
		else:
			location = options['file_location']

		# get raw data
		if location == 'local':
			raw_data = self.get_local_data(file_path)
			header = 'empty'

		if location == 'web':
			raw_data, header = self.get_network_data(file_path)

		# get file type
		if 'file_type' in options.keys():
			file_type = options['file_type']
		else: 
			file_type = file_path.split('.')[len(file_path.split('.'))-1]

		# store raw data in database
		self.write_raw_data_to_database(raw_data, file_type, header, elec_short)

		# import raw data into list of dicts()
		# create data standard
		data = []
		if file_type == 'xml':
			# check, if xml is already downloaded and imported via RawData-hashes
			# if not, convert xml to dict
			root = ET.fromstring(raw_data)

			for mun in root.iter('municipality'):
				tmp = {}
				for elem in mun:
					tmp.update({elem.tag: elem.text})
				data.append(tmp)
		elif file_type == 'txt':
			print('Not yet implemented')
		elif file_type == 'json':
			input_data = json.loads(raw_data)

			for key, value in input_data.items():
				tmp = value
				tmp['municipality_kennzahl'] = key
				data.append(tmp)
		
		# mapping von keys
		if 'mapping_file' in options.keys():
			with open(options['mapping_file']) as data_file:
				mapping = json.loads(data_file.read())

			new_data = []
			for mun in data:
				tmp = {}
				
				for key in mun.keys():
					tmp[mapping[key]] = mun[key]
				new_data.append(tmp)
			data = new_data	
		else: 
			mapping = None
			
		# write election results to database
		timestamp_now = timezone.now()

		party_ids = {}
		for key, value in mapping.items():
			if Party.objects.filter(short_name=value).exists() == True:
				party_ids[value] = Party.objects.get(short_name=value)

		for mun in data:
			if elec_short == 'nrw13':
				time_data = datetime.datetime.now()
				eligible_voters = 0

			elif elec_short == 'nrw17':
				time_data = datetime.datetime.strptime(mun['timestamp'], "%Y-%m-%d %H:%M:%SZ")
				eligible_voters = mun['eligible_voters']
			
			time_data = timezone.make_aware(time_data, timezone.get_current_timezone())

			if Municipality.objects.filter(municipality_kennzahl=mun['municipality_kennzahl']).exists() == True:
				municipality = Municipality.objects.get(municipality_kennzahl=mun['municipality_kennzahl'])
			else:
				municipality = None

			if MunicipalityResult.objects.filter(ts_result=time_data).exists() == False:
				er = MunicipalityResult(
					municipality_id = municipality,
					election_id = election,
					eligible_voters = eligible_voters,
					votes = mun['votes'],
					valid = mun['valid'],
					invalid = mun['invalid'],
					ts_result = time_data,
					is_final = False
				)
				er.save()

				for key, value in party_ids.items():
					if mun[key] == 'None':
						votes = 0
					else:
						votes = int(mun[key])
					pr = PartyResult(
						municipality_result_id = er,
						party_id = value,
						votes = votes
					)
					pr.save()

	def write_raw_data_to_database(self, data, file_type, header, elec_short):
		"""
		Write raw data into table.
		"""
		ts_now = timezone.now()
		election = Election.objects.get(short_name=elec_short)

		raw = RawData(
			timestamp = ts_now,
			hash = hashlib.md5(data.encode()),
			content = data,
			header = header,
			dataformat = file_type,
			election_id = election
		)
		raw.save()

	def get_local_data(self, local_path):
		"""
		Get the data from a local directory.
		"""
		print("Importing data from: {}".format(local_path))
		with open(local_path) as data_file:
			data = data_file.read()

		return data

	def get_network_data(self, url):
		"""
		Get the data from a network location.
		"""

		if url == '':
			print('No import url supplied!')
			return ''

		# make http request
		r = requests.get(url)
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

