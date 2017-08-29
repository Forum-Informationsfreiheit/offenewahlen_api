from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from viz.models import PollingStationResult, RawData, ListResult, PollingStation, RawData, Election, Party, List
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
			'ts_import': timezone.now(),
			'description': 'none',
			'log_detail': 'middle'
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
		data, config['list_objects'] = self.map_keys(data, options)
			
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
		
		raw = RawData(
			ts_import = config['ts_import'],
			ts_file = ts_file,
			hash = hashlib.md5(data.encode()),
			content = data,
			header = header,
			dataformat = config['file_type'],
			description = config['description'],
			election = config['election_object']
		)
		raw.save()

		print('Rawdata imported.')

	def get_local_data(self, local_path):
		"""
		Get the data from a local directory.
		"""
		print('Importing data from: {}'.format(local_path))
		with open(local_path) as data_file:
			data = data_file.read()

		return data

	def get_network_data(self, url):
		"""
		Get the data from a network location.
		"""

		if url == '':
			print('Error: No import url supplied.')
			return ''

		# make http request
		print('Importing data from: {}'.format(url))
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
			print('Warning: Not yet implemented')
		
		elif config['file_type'] == 'json':
			input_data = json.loads(raw_data)

			for key, value in input_data.items():
				tmp = value
				tmp['municipality_code'] = key
				data.append(tmp)

		return data

	def map_keys(self, data, options):
		"""
		Maps keys of input data to database.
		"""

		not_list = ['id', 'municipality_code', 'municipality_kennzahl', 'invalid', 'valid', 'votes', 'timestamp', 'eligible_voters']

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
			list_ids = {}
			for key, value in mapping.items():
				if value not in not_list:
					try:
						list_ids[value] = List.objects.get(short_name=value)
					except:
						print('Error: List "{}" does not exist.'.format(value))

		return new_data, list_ids

	def import_results(self, data, config):
		"""
		Imports results to database.
		"""

		not_found = []
		timestamp_now = timezone.now()
		psr_num_entries_updated = 0
		psr_num_entries_created = 0
		lr_num_entries_updated = 0
		lr_num_entries_created = 0

		for mun in data:
			mun_code = mun['municipality_code']

			# check which election
			if config['election_short'] == 'nrw13':
				ts = datetime.datetime.strptime('2013-09-29', '%Y-%m-%d')
				eligible_voters = None
				config['is_final_master'] = True

			elif config['election_short'] == 'nrw17':
				ts = datetime.datetime.strptime(mun['timestamp'], '%Y-%m-%d %H:%M:%SZ')
				eligible_voters = mun['eligible_voters']
				config['is_final_master'] = False
			
			ts = timezone.make_aware(ts, timezone.get_current_timezone())

			# get polling station
			if len(mun_code) == 6:
				mun_code = mun_code[1:6]
			not_country = not mun_code[:1] == '0'
			not_state = not mun_code[1:5] == '0000'
			not_red = mun_code[1:2].isdigit()
			not_district = not mun_code[3:5] == '00'
			not_absentee_ballot = not mun_code[3:5] == '99'

			if not_country and not_state and not_red and not_district and not_absentee_ballot:
				try:
					ps = PollingStation.objects.get(municipality__code=mun['municipality_code'])
					psr = PollingStationResult.objects.update_or_create(
						polling_station = ps,
						election = config['election_object'],
						eligible_voters = eligible_voters,
						votes = mun['votes'],
						valid = mun['valid'],
						invalid = mun['invalid'],
						ts_result = ts,
						is_final = config['is_final_master']
					)
					if psr[1] == True:
						if config['log_detail'] == 'high':
							print('New pollingstationresult entry "'+psr[0]+'" created.')
						psr_num_entries_created += 1
					else:
						if config['log_detail'] == 'high':
							print('Pollingstationresult entry "'+psr[0]+'" updated.')
						psr_num_entries_updated += 1

					for key, value in config['list_objects'].items():
						if mun[key] == 'None':
							votes = None
						else:
							votes = mun[key]
						
						lr = ListResult.objects.update_or_create(
							polling_station_result = psr[0],
							election_list = value,
							votes = votes
						)
						if lr[1] == True:
							if config['log_detail'] == 'high':
								print('New listresult entry "'+lr[0]+'" created.')
							lr_num_entries_created += 1
						else:
							if config['log_detail'] == 'high':
								print('listresult entry "'+lr[0]+'" updated.')
							lr_num_entries_updated += 1

				except Exception as e:
					if config['log_detail'] == 'middle' and config['log_detail'] == 'high':
						print('Warning: pollingstation {} not found.'.format(mun['municipality_code']))
					not_found.append(mun['municipality_code'])

		print('Pollingstationresult table imported: '+ 'new entries: '+str(psr_num_entries_created)+', updated entries: '+str(psr_num_entries_updated))
		print('Listresult table imported: '+ 'new entries: '+str(lr_num_entries_created)+', updated entries: '+str(lr_num_entries_updated))
		print('Following municipalities where not found:',not_found)	
