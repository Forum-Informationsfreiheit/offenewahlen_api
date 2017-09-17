from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status


class APITest(APITestCase):
	def test_api_root(self):
		"""
		Test if API root can be reached.
		"""
		url = reverse('api-root')
		response = self.client.get(url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

