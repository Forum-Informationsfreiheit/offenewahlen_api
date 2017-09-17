from django.urls import reverse
from django.core.management import call_command
from django.test import Client, TestCase
from rest_framework import status
import os

class FrontendTest(TestCase):

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
			
	def test_viz(self):
		"""
		Test if API root can be reached.
		"""
		url = reverse('viz_overview')
		response = self.client.get(url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)


	def test_viz_results_bar(self):
		"""
		Test if API root can be reached.
		"""
		url = reverse('viz_results_bar')
		response = self.client.get(url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_viz_results_map(self):
		"""
		Test if API root can be reached.
		"""
		url = reverse('viz_results_map')
		response = self.client.get(url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_viz_results_mapnrw13(self):
		"""
		Test if API root can be reached.
		"""
		url = reverse('viz_results_mapnrw13')
		response = self.client.get(url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_viz_results_mapcanvas(self):
		"""
		Test if API root can be reached.
		"""
		url = reverse('viz_results_mapcanvas')
		response = self.client.get(url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_viz_results_timeseries(self):
		"""
		Test if API root can be reached.
		"""
		url = reverse('viz_results_timeseries')
		response = self.client.get(url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

