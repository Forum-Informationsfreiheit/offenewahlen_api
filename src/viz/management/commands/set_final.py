from django.core.management.base import BaseCommand, CommandError
from viz.models import Election

class Command(BaseCommand):

	help = 'Set is_final for an election'

	def add_arguments(self, parser):
		parser.add_argument(
			'election',
			nargs='?'
			)

	def handle(self, *args, **options):

		election_exists = Election.objects.filter(short_name=options['election']).exists()
		if election_exists == True:
			e = Election.objects.get(short_name=options['election'])
			e.is_final = True
			e.save()
		else:
			print('Error: Election is not in database!')
