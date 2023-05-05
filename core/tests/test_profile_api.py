from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from core.tests.custom_test_case import CustomTestCase


class APIUrlsTests(TestCase):

    def test_get_profile_url(self):
        url = reverse('profile-list')
        self.assertEqual(url, '/core/profile/')

    def test_patch_profile_url(self):
        url = reverse('profile-detail', args=[1])
        self.assertEqual(url, '/core/profile/1/')


class ProfileAPIViewTests(CustomTestCase):

    def test_get_profile_authenticated(self):
        url = reverse('profile-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_profile_unauthenticated(self):
        self.client.credentials()
        url = reverse('profile-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
