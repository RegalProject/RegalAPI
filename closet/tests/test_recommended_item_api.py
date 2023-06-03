from django.urls import reverse
from django.conf import settings
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile

from closet.tests.custom_test_case import CustomTestCase
from closet.models import OwnedItem, CrawledItem, Type, Material, Occasion, Brand


import os


class RecommendedItemViewTest(CustomTestCase):

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

    def test_list_recommended_item_authenticated(self):
        url = reverse('recommendedItem-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_recommended_item_unauthenticated(self):
        self.client.force_authenticate(user=None, token=None)
        url = reverse('recommendedItem-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_detail_recommended_item_authenticated(self):  # bug
        url = reverse('crawledItem-detail', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_detail_recommended_item_unauthenticated(self):
        self.client.force_authenticate(user=None, token=None)
        url = reverse('crawledItem-detail', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)