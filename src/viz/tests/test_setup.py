import datetime
import os

from django.test import Client, TestCase
from django.core.management import call_command

from viz.models import Municipality


class SetupTest(TestCase):

	"""
	Test different aspects of the setup process.
	"""

	def test_call_setup_command(self):
		"""
		Calls the setup command.
		"""
		test_path = os.path.dirname(os.path.realpath(__file__))
		test_setup_dir = test_path + '/data/setup/'

		call_command('import_base', test_setup_dir)
		self.assertEqual(1, Municipality.objects.filter(
			name='Gießhübl').count())
