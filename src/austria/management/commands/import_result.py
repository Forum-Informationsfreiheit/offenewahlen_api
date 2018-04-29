from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from austria.models import PollingStation, Election, Party, List, Municipality, District, RegionalElectoralDistrict, State, PollingStationResult, ListResult
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

		# import election results from file
		data = self.open_results_file(config['file_path'])

		# mapping of input data keys to database property names
		data = self.map_keys(data, config)

		# get lists queryset
		config['lists_queryset'] = self.get_lists_queryset(data, config)

		# write election results to database
		self.import_results(data, config)

	def open_results_file(self, local_path):
		"""
		Get the data from a local directory.
		"""
		print('Importing data from: {}'.format(local_path))
		with open(local_path) as data_file:
			data = json.loads(data_file.read())

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
						print('Warning: PollingStation {} not found.'.format(mun['municipality_code']))
					ps_not_found.append(mun['municipality_code'])
			else:
				print('Municipality ' + mun_code + ' not stored in database, cause no municipality.')

		config['psr-entries_created'] = psr_num_entries_created
		config['psr-entries_updated'] = psr_num_entries_updated
		config['lr-entries_created'] = lr_num_entries_created
		config['lr-entries_updated'] = lr_num_entries_updated
		print('PollingStationResult table imported: '+ 'new entries: '+str(psr_num_entries_created)+', updated entries: '+str(psr_num_entries_updated))
		print('ListResult table imported: '+ 'new entries: '+str(lr_num_entries_created)+', updated entries: '+str(lr_num_entries_updated))
		print('These polling stations where not found:', ps_not_found)

	# def compute_aggregates(self, config):
	# 	"""
	# 	Compute aggregates from results
	# 	"""
	#
	# 	ele = config['election_queryset']
	# 	# next: von ListResult auf PollingStationResult gehen und dann auch partei stimmen raus holen und aufsummieren
	# 	data = PollingStationResult.objects.select_related('polling_station__municipality__district__state', 'polling_station__municipality__regional_electoral_district').all().filter(election=ele)
	# 	municipalities = []
	# 	for mun in data:
	# 		tmp = {}
	# 		tmp['votes'] = int(mun.votes)
	# 		tmp['valid'] = int(mun.valid)
	# 		tmp['invalid'] = int(mun.invalid)
	# 		tmp['mun_code'] = str(mun.polling_station.municipality)
	# 		tmp['dis_code'] = str(mun.polling_station.municipality.district)
	# 		tmp['red_code'] = str(mun.polling_station.municipality.regional_electoral_district)
	# 		tmp['state_code'] = str(mun.polling_station.municipality.district.state)
	# 		municipalities.append(tmp)
	# 	df = pd.DataFrame(municipalities)
	# 	df['election'] = config['election_queryset']
	# 	print(df)
	# 	dis = df.groupby('dis_code').sum()
	# 	red = df.groupby('red_code').sum()
	# 	state = df.groupby('state_code').sum()
	# 	#print(dis)
	# 	#print(red)
	# 	#print(state)
	# 	red_entries = red.T.to_dict()
	# 	dis_entries = dis.T.to_dict()
	# 	state_entries = state.T.to_dict()
	# 	#print(dis_entries)
	# 	#print(red_entries)
	# 	#print(state_entries)
	#
	# 	#DistrictResult.objects.bulk_create(dis_entries)
	# 	#REDResult.objects.bulk_create(red_entries)
	# 	#StateResult.objects.bulk_create(state_entries)
	#
	# 	#ListDistrictResult
	# 	#ListREDResult
	# 	#ListStateResult
