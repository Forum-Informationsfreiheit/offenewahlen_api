from django.test import Client, TestCase
from django.conf import settings


class ViewTest(TestCase):

	"""
	Simple test for views.
	"""

	def setUp(self):
		"""
		Set up the test class.
		"""
		self.client = Client()

	def test_index(self):
		"""
		Test the index view.
		"""
		response = self.client.get('/')
		self.assertEqual(response.status_code, 200)
