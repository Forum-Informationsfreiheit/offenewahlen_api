import datetime
import os
from django.test import Client, TestCase
from django.core.management import call_command
from austria.models import Municipality


class SetupTest(TestCase):

	"""
	Test different aspects of the setup process.
	"""

	def test_call_setup_command(self):
		"""
		Calls the setup command.
		"""
		basedata_dir = os.path.dirname(os.path.realpath(__name__)) + '/data/base/'

		call_command('import_basedata', basedata_dir)
		self.assertEqual(1, Municipality.objects.filter(
			name='Gießhübl').count())
