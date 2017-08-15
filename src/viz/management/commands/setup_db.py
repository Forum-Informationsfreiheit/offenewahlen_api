from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from viz.models import Municipality, Election, Party, RegionalElectoralDistrict
import json
import datetime

class Command(BaseCommand):

	help = 'Imports basic data'

	def handle(self, *args, **options):

		# import elections
		with open('../data/setup/elections.json') as data_file:
			elections = json.loads(data_file.read())

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

		# import parties
		with open('../data/setup/parties.json') as data_file:
			parties = json.loads(data_file.read())

		for party in parties:

			if Party.objects.filter(short_name=party['short_name']).exists() == False:
				p = Party(
					wikidata_id = party['wikidata_id'],
					full_name = party['full_name'],
					short_name = party['short_name'],
					family = party['family'],
					website = party['website']
				)
				p.save()

		# import regional electoral districts
		with open('/my-data/projects/okfn/offene-wahlen/github_offenewahlen-nrw17/data/setup/regional-electoral-districts_20170101.json') as data_file:
			reds = json.loads(data_file.read())

		for key, value in reds.items():
			if RegionalElectoralDistrict.objects.filter(short_name=key).exists() == False:
				red = RegionalElectoralDistrict(
					short_name = key,
					full_name = val
				)
				red.save()

		# import municipalities with regional electoral districts
		with open('../data/setup/municipalities_20170101_2.json') as data_file:
			municipalities = json.loads(data_file.read())
		
		with open('../data/setup/reds2municipalities_20170101.json') as data_file:
			red2muns = json.loads(data_file.read())

		for mun in municipalities:
			if Municipality.objects.filter(municipality_kennzahl=mun['municipality_kennzahl']).exists() == False:
				red = RegionalElectoralDistrict.objects.get(short_name=red2muns[mun['municipality_code']])
				
				m = Municipality(
					municipality_kennzahl = mun['municipality_kennzahl'],
					municipality_code = mun['municipality_code'],
					name = mun['name'],
					district = mun['district'],
					regional_electoral_district_id = red,
					state = mun['state']
				)
				m.save()

		# # import states2districts_20170101.json
		# with open('/my-data/projects/okfn/offene-wahlen/github_offenewahlen-nrw17/data/setup/states2districts_20170101.json') as data_file:
		# 	s2d = json.loads(data_file.read())

		# for mun in s2d:

		# 	if Municipality.objects.filter(municipality_kennzahl=mun['municipality_kennzahl']).exists() == False:
		# 		m = Municipality(
		# 			municipality_kennzahl = mun['municipality_kennzahl'],
		# 			municipality_code = mun['municipality_code'],
		# 			name = mun['name'],
		# 			district = mun['district'],
		# 			#regional_electoral_district_id = mun['regional_electoral_district'],
		# 			state = mun['state']
		# 		)
		# 		m.save()
	
