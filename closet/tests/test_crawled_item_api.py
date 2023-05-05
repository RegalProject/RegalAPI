from django.urls import reverse
from django.conf import settings
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile

from closet.tests.custom_test_case import CustomTestCase
from closet.models import OwnedItem, CrawledItem, Type, Material, Occasion, Brand

import os


class CrawledItemViewTest(CustomTestCase):

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
            url='https://test.com/'
        )

        self.crawled_item.material.set([self.material1, self.material2])
        self.crawled_item.occasion.set([self.occasion1, self.occasion2])

    def setUp(self):
        super().setUp()
        self.post_setUp()

    def test_get_crawled_item_authenticated(self):
        url = reverse('crawledItem-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_crawled_item_unauthenticated(self):
        self.client.force_authenticate(user=None, token=None)
        url = reverse('crawledItem-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_crawled_item_authenticated(self):
        url = reverse('crawledItem-list')
        response = self.client.post(url, {
            'name': 'test',
            'season': 'Spring',
            'image': SimpleUploadedFile('test.jpg', self.image_content, content_type='image/jpeg'),
            'color': 'test blue',
            'type': 1,
            'brand': 1,
            'material': [1, 2],
            'occasion': [1, 2],
            'price': 100,
            'url': 'https://test2.com/'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_crawled_item_unauthenticated(self):
        self.client.force_authenticate(user=None, token=None)
        self.test_post_crawled_item_authenticated()

    def test_patch_crawled_item_authenticated(self):
        url = reverse('crawledItem-detail', args=[1])
        response = self.client.patch(url, {'price': 50})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_patch_crawled_item_unauthenticated(self):
        self.client.force_authenticate(user=None, token=None)
        url = reverse('crawledItem-detail', args=[1])
        response = self.client.patch(url, {'price': 50})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_put_crawled_item_authenticated(self):
        url = reverse('crawledItem-detail', args=[1])
        response = self.client.put(url, {
            'name': 'test',
            'season': 'Spring',
            'image': SimpleUploadedFile('test.jpg', self.image_content, content_type='image/jpeg'),
            'color': 'test red',
            'type': 1,
            'brand': 1,
            'material': [1, 2],
            'occasion': [1, 2],
            'price': 100,
            'url': 'https://test.com/'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_crawled_item_unauthenticated(self):
        self.client.force_authenticate(user=None, token=None)
        self.test_put_crawled_item_authenticated()

    def test_delete_crawled_item_authenticated(self):
        url = reverse('crawledItem-detail', args=[1])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_crawled_item_unauthenticated(self):
        self.client.force_authenticate(user=None, token=None)
        url = reverse('crawledItem-detail', args=[1])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

