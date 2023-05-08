from django.urls import reverse
from django.conf import settings
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile

from closet.tests.custom_test_case import CustomTestCase
from closet.models import OwnedItem, CrawledItem, Type, Material, Occasion, Brand


import os

class WishlistViewTest(CustomTestCase):
    
    def post_setUp(self):
        pass
        #to be fixed
        
    def setUp(self):
        super().setUp()
        self.post_setUp()
        
    def test_get_wishlist_authenticated(self):
        url = reverse('wishlist-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_wishlist_unauthenticated(self):
        self.client.force_authenticate(user=None, token=None)
        url = reverse('wishlist-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_delete_wishlist_authenticated(self):
        url = reverse('wishlist-detail', args=[1])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_delete_wishlist_unauthenticated(self):
        self.client.force_authenticate(user=None, token=None)
        url = reverse('wishlist-detail', args=[1])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_post_wishlist_authenticated(self):
        url = reverse('wishlist-list')
        response = self.client.post(url, {
            'items': [1]
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_post_wishlist_unauthenticated(self):
        self.client.force_authenticate(user=None, token=None)
        url = reverse('wishlist-list')
        response = self.client.post(url, {
            'items': [1]
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    