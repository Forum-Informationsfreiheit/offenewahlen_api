from django.urls import reverse
from django.core.management import call_command
from django.test import Client, TestCase
from rest_framework import status
import os

class DatadeliveryTest(TestCase):

	def setUp(self):
		"""
		Set up the test class.

		For the import to run an election has to exist in the
		database.
		"""

		#call_command('import_basedata')
		#test_path = setup_path = os.path.dirname(os.path.realpath(__file__))
		#results_file = test_path + '/data/example_01.json'
		#mapping_file = test_path + '/data/example_config.json'
		#call_command('import_results', results_file, mapping_file)
			
	def test_csv_export(self):
		"""
		Test if API root can be reached.
		"""
		url = reverse('serve_nrw13_csv')
		response = self.client.get(url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_geom_export(self):
		"""
		Test if API root can be reached.
		"""
		url = reverse('api_geom')
		response = self.client.get(url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

