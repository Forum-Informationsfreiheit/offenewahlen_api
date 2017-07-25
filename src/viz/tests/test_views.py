from unittest import TestCase
from django.test import Client


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
		self.assertEqual(response.status_code, 302)

		response = self.client.get('/de')
		self.assertEqual(response.status_code, 301)

		response = self.client.get('/de/')
		self.assertEqual(response.status_code, 200)

