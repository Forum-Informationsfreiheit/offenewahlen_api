from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from viz.models import PollingStationResult, RawData, ListResult, \
	PollingStation, RawData, Election, Party, List
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
			'result_file',
			nargs='?'
		)
		parser.add_argument(
			'config_file',
			nargs='?'
		)

	def handle(self, *args, **options):
		
		# open config file
		with open(options['config_file']) as config_file:
			config = json.loads(config_file.read())
		
		config['file_path'] = options['result_file']
		config['election_queryset'] = Election.objects.get(short_name=config['election_short'])
		config['ts_import'] = timezone.now()
		config['log_detail'] = 'middle'

		# get raw data
		if config['file_location'] == 'local':
			raw_data = self.get_local_data(config['file_path'])
			header = None
		elif config['file_location'] == 'web':
			(raw_data, header) = self.get_network_data(config['file_path'])

		# store raw data in database
		self.write_raw_data_to_database(raw_data, header, config)

		# convert different raw data types to uniform data standard
		data = self.standardize_raw_data(raw_data, config)	

		# mapping of input data keys to database property names
		data = self.map_keys(data, config)
			
		# get lists queryset
		config['lists_queryset'] = self.get_lists_queryset(data, config)
			
		# write election results to database
		self.import_results(data, config)

	def write_raw_data_to_database(self, data, header, config, ts_file=None):
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
			election = config['election_queryset']
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

		output:
		- 
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

			if config['data_format'] == 'ow-at':
				for key, val in input_data.items():
					tmp = val
					tmp[config['spatial_id']] = key
					data.append(tmp)
			elif config['data_format'] == 'bmi':
				data = input_data

		return data

	def map_keys(self, data, config):
		"""
		Maps keys of input data to database.
		"""
		
		new_data = []

		# map the keys
		mappings = config['mappings']
		for mun in data:
			tmp = {}
			for key in mun.keys():
				tmp[mappings[key]] = mun[key]
			new_data.append(tmp)

		return new_data

	def get_lists_queryset(self, data, config):
		# get party querysets
		mappings = config['mappings']
		lists_queryset = {}
		
		for key, val in mappings.items():
			if val not in config['no_list']:
				try:
					lists_queryset[val] = List.objects.get(short_name=val)
				except:
					print('Error: Electoral List "{}" does not exist.'.format(val))

		return lists_queryset

	def import_results(self, data, config):
		"""
		Imports results to database.
		"""

		ps_not_found = []
		psr_num_entries_created = 0
		psr_num_entries_updated = 0
		lr_num_entries_created = 0
		lr_num_entries_updated = 0

		for mun in data:
			mun_code = mun[config['spatial_id']]
			elec_short = config['election_short']

			# get timestamp of election result and convert it to server timezone
			if 'timestamp' in config:
				ts = datetime.datetime.strptime(config['timestamp'], '%Y-%m-%d %H:%M:%SZ')
			else:
				ts = datetime.datetime.strptime(mun['timestamp'], '%Y-%m-%d %H:%M:%SZ')
			ts = timezone.make_aware(ts, timezone.get_current_timezone())

			# Get eligible voters. Set to none if not in results
			if config['eligible_voters']:
				eligible_voters = mun['eligible_voters']
			else: 
				eligible_voters = None

			# check type of polling station: municipality, regional_electoral_district, state, district, country
			if len(mun_code) == 6:
				mun_code = mun_code[1:6]
				if config['log_detail'] == 'high':
					print("Municipality code shortened from 6 to 5 digits.")
			not_country = not mun_code[:1] == '0'
			not_state = not mun_code[1:5] == '0000'
			not_red = mun_code[1:2].isdigit()
			not_district = not mun_code[3:5] == '00'
			not_absentee_ballot = not mun_code[3:5] == '99'

			if not_country and not_state and not_red and not_district and not_absentee_ballot:
				try:
					if config['spatial_id'] == 'municipality_code':
						ps = PollingStation.objects.get(municipality__code=mun['municipality_code'])
					elif config['spatial_id'] == 'municipality_kennzahl':
						ps = PollingStation.objects.get(municipality__kennzahl=mun['municipality_kennzahl'])
					psr = PollingStationResult.objects.update_or_create(
						polling_station = ps,
						election = config['election_queryset'],
						eligible_voters = eligible_voters,
						votes = mun['votes'],
						valid = mun['valid'],
						invalid = mun['invalid'],
						ts_result = ts
					)
					if psr[1] == True:
						if config['log_detail'] == 'high':
							print('New pollingStationResult "'+psr[0]+'" created.')
						psr_num_entries_created += 1
					else:
						if config['log_detail'] == 'high':
							print('PollingStationResult "'+psr[0]+'" updated.')
						psr_num_entries_updated += 1

					for key, value in config['lists_queryset'].items():
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
								print('New ListResult "'+lr[0]+'" created.')
							lr_num_entries_created += 1
						else:
							if config['log_detail'] == 'high':
								print('ListResult "'+lr[0]+'" updated.')
							lr_num_entries_updated += 1

				except Exception as e:
					if config['log_detail'] == 'middle' and config['log_detail'] == 'high':
						print('Warning: PollingStation {} not found.'.format(mun[config['spatial_id']]))
					ps_not_found.append(mun[config['spatial_id']])
			else:
				print('Municipality ' + mun_code + ' not stored in database, cause no municipality.')

		config['psr-entries_created'] = psr_num_entries_created
		config['psr-entries_updated'] = psr_num_entries_updated
		config['lr-entries_created'] = lr_num_entries_created
		config['lr-entries_updated'] = lr_num_entries_updated
		print('PollingStationResult table imported: '+ 'new entries: '+str(psr_num_entries_created)+', updated entries: '+str(psr_num_entries_updated))
		print('ListResult table imported: '+ 'new entries: '+str(lr_num_entries_created)+', updated entries: '+str(lr_num_entries_updated))
		print('These polling stations where not found:', ps_not_found)	
