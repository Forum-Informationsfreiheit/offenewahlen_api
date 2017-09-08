import datetime
import os

from unittest import TestCase
from django.test import Client
from django.core.management import call_command
from django.utils import timezone

from viz.models import RawData, Election


class ImportTest(TestCase):

	"""
	Simple test for views.
	"""

	def setUp(self):
		"""
		Set up the test class.
		"""
		election_time = datetime.datetime.strptime('2017-01-01', '%Y-%m-%d')
		election_time = timezone.make_aware(election_time,
				timezone.get_current_timezone())

		Election.objects.update_or_create(
			short_name = 'nrw17',
			short_name_text = '',
			full_name = '',
			election_type = '',
			wikidata_id = '',
			administrative_level = '',
			election_day = election_time
		)

	def test_run(self):
		test_path = os.path.dirname(os.path.realpath(__file__))
		local_data_file = test_path + '/data/test_data.xml'
		mapping_file = test_path + '/data/nrw_2017_mapping.json'

		call_command('import_results', local_data_file, location='local',
			file_type='xml', mapping_file=mapping_file)
		number_of_results = RawData.objects.count()
		self.assertEqual(number_of_results, 1)

		call_command('import_results', local_data_file, location='local',
			file_type='xml', mapping_file=mapping_file)
		number_of_results = RawData.objects.count()
		self.assertEqual(number_of_results, 2)

