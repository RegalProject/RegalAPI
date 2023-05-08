from django.urls import reverse
from django.conf import settings
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile

from closet.tests.custom_test_case import CustomTestCase
from closet.models import OwnedItem, CrawledItem, Type, Material, Occasion, Brand


import os

class RecommendedItemViewTest(CustomTestCase):
    
    def test_list_recommended_item_authenticated(self):
        url = reverse('recommendedItem-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_recommended_item_unauthenticated(self):
        self.client.force_authenticate(user=None, token=None)
        url = reverse('recommendedItem-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_detail_recommended_item_authenticated(self):
        url = reverse('crawledItem-detail', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_detail_recommended_item_unauthenticated(self):
        self.client.force_authenticate(user=None, token=None)
        url = reverse('crawledItem-detail', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)