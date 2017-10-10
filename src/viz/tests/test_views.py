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
		self.assertEqual(response.status_code, 302)

	# def test_index_locales(self):
	# 	"""
	# 	Test index in all locales specified in settings.
	# 	"""
	# 	for language in settings.LANGUAGES:
	# 		locale = language[0]
	#
	# 		response = self.client.get('/{}'.format(locale))
	# 		self.assertEqual(response.status_code, 301)
	#
	# 		response = self.client.get('/{}/'.format(locale))
	# 		self.assertEqual(response.status_code, 200)

	# def test_non_existant_locale(self):
	# 	"""
	# 	Tests a non-existant locale. Currently 404 response.
	# 	"""
	# 	response = self.client.get('/fr')
	# 	self.assertEqual(response.status_code, 404)
	#
	# 	response = self.client.get('/fr/')
	# 	self.assertEqual(response.status_code, 404)
