from django.urls import reverse
from django.core.management import call_command
from rest_framework.test import APITestCase
from rest_framework import status
import os

class APITest(APITestCase):

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
			
	def test_api_root(self):
		"""
		Test if API root can be reached.
		"""
		url = reverse('api-root')
		response = self.client.get(url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_api_result(self):
		"""
		Test if API result/ can be reached.
		"""
		url = reverse('result-list')
		response = self.client.get(url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_api_election(self):
		"""
		Test if API result/ can be reached.
		"""
		url = reverse('election-list')
		response = self.client.get(url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_api_party(self):
		"""
		Test if API result/ can be reached.
		"""
		url = reverse('party-list')
		response = self.client.get(url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_api_list(self):
		"""
		Test if API result/ can be reached.
		"""
		url = reverse('list-list')
		response = self.client.get(url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_api_polling_station(self):
		"""
		Test if API result/ can be reached.
		"""
		url = reverse('polling_station-list')
		response = self.client.get(url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_api_municipality(self):
		"""
		Test if API result/ can be reached.
		"""
		url = reverse('municipality-list')
		response = self.client.get(url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_api_district(self):
		"""
		Test if API result/ can be reached.
		"""
		url = reverse('district-list')
		response = self.client.get(url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_api_state(self):
		"""
		Test if API result/ can be reached.
		"""
		url = reverse('state-list')
		response = self.client.get(url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_api_red(self):
		"""
		Test if API result/ can be reached.
		"""
		url = reverse('regional_electoral_district-list')
		response = self.client.get(url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

