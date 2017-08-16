from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from viz.models import PollingStationResult, RawData, PartyResult, PollingStation, RawData, Election, Party
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
		
		config = {
			'file_path': options['file'],
			'election_short': options['election'],
			'election_object': Election.objects.get(short_name=options['election']),
			'file_location': None,
			'ts_import': timezone.now()
		}

		config['file_location'] = self.get_file_location(config)

		# get raw data
		if config['file_location'] == 'local':
			raw_data = self.get_local_data(config['file_path'])
			header = None

		if config['file_location'] == 'web':
			raw_data, header = self.get_network_data(config['file_path'])

		# get file type
		config['file_type'] = self.get_file_type(options)

		# store raw data in database
		self.write_raw_data_to_database(raw_data, header, config)

		# convert different raw data types to uniform data standard
		data = self.standardize_raw_data(raw_data, config)		

		# map keys of input data to database
		data, config['party_objects'] = self.map_keys(data, options)
			
		# write election results to database
		self.import_results(data, config)

	def get_file_location(self, config):
		"""
		Get the location where the file is stored (web or local)
		"""

		if config['file_location'] == None:
			if config['file_path'][:4] == 'http' or config['file_path'][:3] == 'ftp':
				file_location = 'web'
			else:
				file_location = 'local'
		else:
			file_location = options['file_location']

		return file_location


	def get_file_type(self, options):
		"""
		Get file type from file path.
		"""

		if 'file_type' in options.keys():
			file_type = options['file_type']
		else: 
			file_type = file_path.split('.')[len(file_path.split('.'))-1]

		return file_type

	def write_raw_data_to_database(self, data, header,config, ts_file=None):
		"""
		Write raw data into table.
		"""
		
		election = Election.objects.get(short_name=config['election_short'])

		raw = RawData(
			ts_import = config['ts_import'],
			ts_file = ts_file,
			hash = hashlib.md5(data.encode()),
			content = data,
			header = header,
			dataformat = config['file_type'],
			election = election
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
		print("Importing data from: {}".format(url))
		r = requests.get(url)

		return (r.text, r.headers)

	def standardize_raw_data(self, raw_data, config):
		"""
		Converts the raw data from different inputs to same data format (list of dicts())
		"""

		data = []
		if config['file_type'] == 'xml':
			# check, if xml is already downloaded and imported via RawData-hashes
			# if not, convert xml to dict
			root = ET.fromstring(raw_data)

			for mun in root.iter('municipality'):
				tmp = {}
				for elem in mun:
					tmp.update({elem.tag: elem.text})
				data.append(tmp)
		
		elif config['file_type'] == 'txt':
			print('Not yet implemented')
		
		elif config['file_type'] == 'json':
			input_data = json.loads(raw_data)

			for key, value in input_data.items():
				tmp = value
				tmp['municipality_kennzahl'] = key
				data.append(tmp)

		return data

	def map_keys(self, data, options):
		"""
		Maps keys of input data to database.
		"""

		if 'mapping_file' in options.keys():
			with open(options['mapping_file']) as data_file:
				mapping = json.loads(data_file.read())

			new_data = []
			for mun in data:
				tmp = {}
				
				for key in mun.keys():
					tmp[mapping[key]] = mun[key]
				new_data.append(tmp)

			# get party objects
			party_ids = {}
			for key, value in mapping.items():
				party_exists = Party.objects.filter(short_name=value).exists()
				if  party_exists == True:
					party_ids[value] = Party.objects.get(short_name=value)
				else:
					print('Error: Party "{}" does not exist.'.format(value))

		return new_data, party_ids

	def import_results(self, data, config):
		"""
		Imports results to database.
		"""

		timestamp_now = timezone.now()

		for mun in data:

			# check which election
			if config['election_short'] == 'nrw13':
				time_data = datetime.datetime.strptime('2013-09-29', '%Y-%m-%d')
				eligible_voters = None
				config['is_final_master'] = True

			elif config['election_short'] == 'nrw17':
				time_data = datetime.datetime.strptime(mun['timestamp'], '%Y-%m-%d %H:%M:%SZ')
				eligible_voters = mun['eligible_voters']
				config['is_final_master'] = False
			
			time_data = timezone.make_aware(time_data, timezone.get_current_timezone())

			# get polling station
			municipality_kennzahl_exists = PollingStation.objects.filter(municipality_kennzahl=mun['municipality_kennzahl']).exists()
			if municipality_kennzahl_exists == True:
				polling_station = PollingStation.objects.get(municipality_kennzahl=mun['municipality_kennzahl'])
			else:
				print('Warning: Polling Station {} does not exist!'.format(mun['municipality_kennzahl']))
				polling_station = None

			# check if realtime data or final result
			if config['is_final_master'] == True:
				if polling_station == None:
					result_exists == True
				else:
					result_exists = PollingStationResult.objects.filter(polling_station=polling_station, election=config['election_object']).exists()
			else:
				result_exists = PollingStationResult.objects.filter(ts_result=time_data).exists()

			# import results
			if result_exists == False:
				if polling_station != None:
					psr = PollingStationResult(
						polling_station = polling_station,
						election = config['election_object'],
						eligible_voters = eligible_voters,
						votes = mun['votes'],
						valid = mun['valid'],
						invalid = mun['invalid'],
						ts_result = time_data,
						is_final = config['is_final_master']
					)
					psr.save()

					for key, value in config['party_objects'].items():
						if mun[key] == 'None':
							votes = None
						else:
							votes = mun[key]
						pr = PartyResult(
							polling_station_result = psr,
							party = value,
							votes = votes
						)
						pr.save()
			#else:
			#	print('Warning: Result already exists.')


