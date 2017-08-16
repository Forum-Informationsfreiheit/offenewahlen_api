from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from viz.models import PollingStation, Election, Party, RegionalElectoralDistrict, State, District
import json
import datetime

class Command(BaseCommand):

	help = 'Import basic data into database'

	def handle(self, *args, **options):

		config = {
			'party_location': 'austria'
		}

		# import elections
		elections = json.loads(self.open_file('../data/setup/elections.json'))
		self.import_elections(elections)

		# import parties
		parties = json.loads(self.open_file('../data/setup/parties.json'))
		self.import_parties(parties, config)

		# import states and districts
		states_districts = json.loads(self.open_file('../data/setup/states2districts_20170101.json'))
		self.import_states_districts(states_districts)

		# import regional electoral districts
		reds = json.loads(self.open_file('../data/setup/regional-electoral-districts_20170101.json'))
		self.import_reds(reds)

		# import municipalities
		municipalities = json.loads(self.open_file('../data/setup/municipalities_20170101_2.json'))
		muns2reds = json.loads(self.open_file('../data/setup/municipalities2reds_20170101.json'))
		self.import_municipalities(municipalities, muns2reds)

	def open_file(self, filename,):
		"""
		Open file.
		"""

		try:
			with open(filename) as data_file:
				return data_file.read()
		except IOError:
			print('Error: can\'t find file or read data')

	def import_elections(self, elections):
		"""
		Import elections data into database.
		"""

		for election in elections:
			time_data = datetime.datetime.strptime(election['election_day'], "%Y-%m-%d")
			time_data = timezone.make_aware(time_data, timezone.get_current_timezone())

			if Election.objects.filter(short_name=election['short_name']).exists() == False:
				e = Election(
					full_name = election['full_name'],
					short_name = election['short_name'],
					election_type = election['election_type'],
					wikidata_id = election['wikidata_id'],
					administrative_level = election['administrative_level'],
					election_day = time_data
				)
				e.save()
			#else:
			#	print('Warning: Election {} already exists.'.format(election['full_name']))

	def import_parties(self, parties, config):
		"""
		Import parties data into database.
		"""

		for party in parties:

			if Party.objects.filter(short_name=party['short_name']).exists() == False:
				p = Party(
					wikidata_id=party['wikidata_id'],
					full_name=party['full_name'],
					short_name=party['short_name'],
					family=party['family'],
					website=party['website'],
					location=config['party_location']
				)
				p.save()
			#else:
			#	print('Warning: Party {} already exists.'.format(party['full_name']))

	def import_reds(self, reds):
		"""
		Import regional electoral districts data into database.
		"""

		for key, value in reds.items():
			if RegionalElectoralDistrict.objects.filter(short_code=key).exists() == False:
				red = RegionalElectoralDistrict(
					name = value,
					short_code = key
				)
				red.save()
			#else:
			#	print('Warning: Regional Electoral District {} already exists.'.format(value))


	def import_municipalities(self, municipalities, muns2reds):
		"""
		Import municipalities as polling stations into database.
		"""

		for mun in municipalities:
			if PollingStation.objects.filter(municipality_kennzahl=mun['municipality_kennzahl']).exists() == False:
				red = RegionalElectoralDistrict.objects.get(short_code=muns2reds[mun['municipality_code']])
				district = District.objects.get(name=mun['district'])

				p = PollingStation(
					municipality_kennzahl = mun['municipality_kennzahl'],
					municipality_code = mun['municipality_code'],
					municipality_name = mun['name'],
					type = 'municipality',
					regional_electoral_district = red,
					district = district
				)
				p.save()
			#else:
			#	print('Warning: PollingStation {} already exists.'.format(mun['municipality_kennzahl']))

	def import_states_districts(self, states_districts):
		"""
		Import states and districts into database.
		"""

		for state_key in states_districts.keys():
			state_exists = State.objects.filter(short_code=state_key).exists()
			if state_exists == False:
				s = State(
					short_code = state_key,
					name = states_districts[state_key]['name']
				)
				s.save()
				state = s
			else:
				#print('State {} already exists.'.format(state_key))
				state = State.objects.get(short_code=state_key)

			for key, value in states_districts[state_key]['districts'].items():
				district_state_exists = District.objects.filter(short_code=key, state=state).exists()
				if district_state_exists == False:
					d = District(
						short_code = key,
						name = value,
						state = s
					)
					d.save()
				#else:
				#	print('Warning: District {} already exists.'.format(value))


	
