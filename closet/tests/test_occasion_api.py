from django.urls import reverse
from django.conf import settings
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile

from closet.tests.custom_test_case import CustomTestCase
from closet.models import OwnedItem, CrawledItem, Type, Material, Occasion, Brand


import os

class OccasionViewTest(CustomTestCase):
    
    def test_get_occasion_authenticated(self):
        url = reverse('occasion-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_occasion_unauthenticated(self):
        self.client.force_authenticate(user=None, token=None)
        url = reverse('occasion-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_post_occasion_authenticated(self):
        url = reverse('occasion-list')
        response = self.client.post(url, {
            'name': 'test_occasion'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_post_occasion_unauthenticated(self):
        self.client.force_authenticate(user=None, token=None)
        url = reverse('occasion-list')
        response = self.client.post(url, {
            'name': 'test_occasion'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    # def test_post_occasion_invalid_name(self):
    #     url = reverse('occasion-list')
    #     response = self.client.post(url, {
    #         'name': 100
    #     })
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_post_occasion_invalid_name_empty(self):
        url = reverse('occasion-list')
        response = self.client.post(url, {
            'name': ''
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_post_occasion_invalid_name_too_long(self):
        url = reverse('occasion-list')
        response = self.client.post(url, {
            'name': 'a' * 257
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    