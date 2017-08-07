import os

from unittest import TestCase
from django.test import Client
from django.core.management import call_command

from viz.models import RawData

class ImportTest(TestCase):

	"""
	Simple test for views.
	"""

	def test_run(self):
		test_path = os.path.dirname(os.path.realpath(__file__))
		local_data_file = test_path + '/data/test_data.xml'
		call_command('importresults', local_path=local_data_file)
		number_of_results = RawData.objects.count()
		self.assertEqual(number_of_results, 1)

		call_command('importresults', local_path=local_data_file)
		number_of_results = RawData.objects.count()
		self.assertEqual(number_of_results, 2)

