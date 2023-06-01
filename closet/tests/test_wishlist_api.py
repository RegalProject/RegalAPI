from django.urls import reverse
from django.conf import settings
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile

from closet.tests.custom_test_case import CustomTestCase
from closet.models import OwnedItem, CrawledItem, Type, Material, Occasion, Brand


import os


class WishlistViewTest(CustomTestCase):

    def post_setUp(self):
        self.image_content = open(os.path.join(settings.MEDIA_ROOT, 'ItemPics/download.jpg'), 'rb').read()

        self.type = Type.objects.create(name='test type')
        self.brand = Brand.objects.create(name='test brand')
        self.material1 = Material.objects.create(name='test material 1')
        self.material2 = Material.objects.create(name='test material 2')
        self.occasion1 = Occasion.objects.create(name='test occasion 1')
        self.occasion2 = Occasion.objects.create(name='test occasion 2')

        self.crawled_item = CrawledItem.objects.create(
            name='test',
            season='Spring',
            image='test.jpg',
            color='test blue',
            type=self.type,
            brand=self.brand,
            price=100,
            url='https://test.com'
        )

        self.crawled_item.material.set([self.material1, self.material2])
        self.crawled_item.occasion.set([self.occasion1, self.occasion2])

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

    def test_delete_wishlist_authenticated(self):
        url = reverse('wishlist-list')
        self.client.post(url, {
            'items': [1]
        })
        url = reverse('wishlist-detail', args=[1])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_delete_wishlist_unauthenticated(self):
        self.client.force_authenticate(user=None, token=None)
        url = reverse('wishlist-detail', args=[1])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    