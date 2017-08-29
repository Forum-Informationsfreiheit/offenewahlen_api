from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from viz.models import PollingStation, Election, Party, RegionalElectoralDistrict, State, District, Municipality, List
import json
import datetime

class Command(BaseCommand):

	help = 'Import basic data into database'

	def handle(self, *args, **options):

		config = {
			'party_location': 'austria',
			'log_detail' : 'low'
		}

		# import elections
		elections = json.loads(self.open_file('data/setup/elections.json'))
		self.import_elections(elections, config)

		# import regional electoral districts
		reds = json.loads(self.open_file('data/setup/regional-electoral-districts_20170101.json'))
		self.import_reds(reds, config)

		# import parties
		parties = json.loads(self.open_file('data/setup/parties.json'))
		self.import_parties(parties, config)
		
		# import lists
		lists = json.loads(self.open_file('data/setup/lists.json'))
		self.import_lists(lists, config)

		# import states and districts
		states_districts = json.loads(self.open_file('data/setup/states-to-districts_20170101.json'))
		self.import_states_districts(states_districts, config)

		# import municipalities
		municipalities = json.loads(self.open_file('data/setup/municipalities_20170101_2.json'))
		muns2reds = json.loads(self.open_file('data/setup/municipality2red_20170101.json'))
		self.import_municipalities(municipalities, muns2reds, config)

	def open_file(self, filename,):
		"""
		Open file.
		"""

		try:
			with open(filename) as data_file:
				return data_file.read()
		except IOError:
			print('Error: can\'t find file or read data')

	def open_jsonfile(self, filename):

		try:
			data = json.loads(self.open_file(filename))
			return data
		except JSONDecodeError:
			print('Error: File is not valid JSON.')

	def import_elections(self, elections, config):
		"""
		Import elections data into database.
		"""

		num_entries_created = 0
		num_entries_updated = 0

		for key, value in elections.items():
			ts = datetime.datetime.strptime(value['election_day'], "%Y-%m-%d")
			ts = timezone.make_aware(ts, timezone.get_current_timezone())

			e = Election.objects.update_or_create(
				short_name = value['short_name'],
				short_name_text = value['short_name_text'],
				full_name = value['full_name'],
				election_type = value['election_type'],
				wikidata_id = value['wikidata_id'],
				administrative_level = value['administrative_level'],
				election_day = ts
			)
			if e[1] == True:
				if config['log_detail'] == 'high':
					print('New election entry "'+value['short_name']+'" created.')
				num_entries_created += 1
			else:
				if config['log_detail'] == 'high':
					print('Election entry "'+value['short_name']+'" updated.')
				num_entries_updated += 1

		print('Election table imported: '+ 'new entries: '+str(num_entries_created)+', updated entries: '+str(num_entries_updated))

	def import_reds(self, reds, config):
		"""
		Import regional electoral districts data into database.
		"""

		num_entries_created = 0
		num_entries_updated = 0

		for key, value in reds.items():
			red = RegionalElectoralDistrict.objects.update_or_create(
				short_code=str(key),
				name = value
			)
			if red[1] == True:
				if config['log_detail'] == 'high':
					print('New regional electoral district entry "'+value+'" created.')
				num_entries_created += 1
			else:
				if config['log_detail'] == 'high':
					print('Regional electoral district entry "'+value+'" updated.')
				num_entries_updated += 1

		print('Regionalelectoraldistrict table imported: '+ 'new entries: '+str(num_entries_created)+', updated entries: '+str(num_entries_updated))

	def import_parties(self, parties, config):
		"""
		Import parties data into database.
		"""

		num_entries_created = 0
		num_entries_updated = 0

		for key, value in parties.items():
			p = Party.objects.update_or_create(
				short_name = value['short_name'],
				short_name_text = value['short_name_text'],
				full_name = value['full_name'],
				family = value['family'],
				wikidata_id = value['wikidata_id'],
				website = value['website'],
				location = config['party_location']
			)
			if p[1] == True:
				if config['log_detail'] == 'high':
					print('New party entry "'+value['short_name']+'" created.')
				num_entries_created += 1
			else:
				if config['log_detail'] == 'high':
					print('Party entry "'+value['short_name']+'" updated.')
				num_entries_updated += 1

		print('Party table imported: '+ 'new entries: '+str(num_entries_created)+', updated entries: '+str(num_entries_updated))

	def import_lists(self, lists, config):
		"""
		Import parties data into database.
		"""

		num_entries_created = 0
		num_entries_updated = 0
		num_lists_notfound = 0

		for key, ele_list in lists.items():
			for lst in ele_list:
				try:
					p = Party.objects.get(short_name = lst['party'])
					l = List.objects.update_or_create(
						short_name = lst['short_name'],
						short_name_text = lst['short_name_text'],
						full_name = lst['full_name'],
						party = p
					)
				except Exception as e:
					if config['log_detail'] == 'middle' or config['log_detail'] == 'high':
						print('Warning: Party not found.')
					num_lists_notfound += 1
					l = List.objects.update_or_create(
						short_name = lst['short_name'],
						short_name_text = lst['short_name_text'],
						full_name = lst['full_name']
					)

				if l[1] == True:
					if config['log_detail'] == 'high':
						print('New list entry "'+lst['short_name']+'" created.')
					num_entries_created += 1
				else:
					if config['log_detail'] == 'high':
						print('List entry "'+lst['short_name']+'" updated.')
					num_entries_updated += 1

		print('List table imported: '+ 'new entries: '+str(num_entries_created)+', updated entries: '+str(num_entries_updated)+', lists not found: '+str(num_lists_notfound))


	def import_states_districts(self, states_districts, config):
		"""
		Import states and districts into database.
		"""

		d_num_entries_created = 0
		d_num_entries_updated = 0
		s_num_entries_created = 0
		s_num_entries_updated = 0

		for s_key, s_val in states_districts.items():
			s = State.objects.update_or_create(
				short_code = str(s_key),
				name = s_val['name']
			)
			
			if s[1] == True:
				if config['log_detail'] == 'high':
					print('New state entry "'+str(s_key)+'" created.')
				s_num_entries_created += 1
			else:
				if config['log_detail'] == 'high':
					print('State entry "'+str(s_key)+'" updated.')
				s_num_entries_updated += 1

			for key, value in s_val['districts'].items():
				d = District.objects.update_or_create(
					short_code=str(key),
					name = value,
					state=s[0]
				)
				if d[1] == True:
					if config['log_detail'] == 'high':
						print('New district entry "'+str(key)+'" created.')
					d_num_entries_created += 1
				else:
					if config['log_detail'] == 'high':
						print('District entry "'+str(key)+'" updated.')
					d_num_entries_updated += 1

		print('State table imported: '+ 'new entries: '+str(s_num_entries_created)+', updated entries: '+str(s_num_entries_updated))
		print('District table imported: '+ 'new entries: '+str(d_num_entries_created)+', updated entries: '+str(d_num_entries_updated))

	def import_municipalities(self, municipalities, muns2reds, config):
		"""
		Import municipalities as polling stations into database.
		"""

		ps_num_entries_created = 0
		ps_num_entries_updated = 0
		m_num_entries_created = 0
		m_num_entries_updated = 0

		for mun in municipalities:

			try:
				red = RegionalElectoralDistrict.objects.get(short_code=muns2reds[mun['municipality_code']])
			except Exception as e:
				if config['log_detail'] == 'middle' or config['log_detail'] == 'high':
					print('Warning: regionalelectoraldistrict not found.')

			try:
				d = District.objects.get(name=mun['district'])
			except Exception as e:
				if config['log_detail'] == 'middle' or config['log_detail'] == 'high':
					print('Warning: district not found.')

			m = Municipality.objects.update_or_create(
				code = str(mun['municipality_code']),
				kennzahl = str(mun['municipality_kennzahl']),
				name = mun['name'],
				regional_electoral_district = red,
				district = d
			)
			if m[1] == True:
				if config['log_detail'] == 'high':
					print('New municipality entry "'+str(mun['name'])+'" created.')
				m_num_entries_created += 1
			else:
				if config['log_detail'] == 'high':
					print('Municipality entry "'+str(mun['name'])+'" updated.')
				m_num_entries_updated += 1

			ps = PollingStation.objects.update_or_create(
				name = mun['name'],
				type = 'municipality',
				municipality = m[0]
			)
			if ps[1] == True:
				if config['log_detail'] == 'high':
					print('New pollingstation entry "'+str(mun['name'])+'" created.')
				ps_num_entries_created += 1
			else:
				if config['log_detail'] == 'high':
					print('Pollingstation entry "'+str(mun['name'])+'" updated.')
				ps_num_entries_updated += 1

		print('Municipality table imported: '+ 'new entries: '+str(m_num_entries_created)+', updated entries: '+str(m_num_entries_updated))
		print('Pollingstation table imported: '+ 'new entries: '+str(ps_num_entries_created)+', updated entries: '+str(ps_num_entries_updated))

