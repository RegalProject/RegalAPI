from django.urls import reverse
from django.conf import settings
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile

from closet.tests.custom_test_case import CustomTestCase
from closet.models import OwnedItem, CrawledItem, Type, Material, Occasion, Brand


import os


class OwnedItemViewTest(CustomTestCase):

    def post_setUp(self):
        self.image_content = open(os.path.join(settings.MEDIA_ROOT, 'ItemPics/download.jpg'), 'rb').read()

        self.type = Type.objects.create(name='test type')
        self.brand = Brand.objects.create(name='test brand')
        self.material1 = Material.objects.create(name='test material 1')
        self.material2 = Material.objects.create(name='test material 2')
        self.occasion1 = Occasion.objects.create(name='test occasion 1')
        self.occasion2 = Occasion.objects.create(name='test occasion 2')

        self.owned_item = OwnedItem.objects.create(
            name='test',
            season='Spring',
            image='test.jpg',
            color='test blue',
            type=self.type,
            brand=self.brand,
            owner=self.user,
            is_public=True,
            score=100
        )

        self.owned_item.material.set([self.material1, self.material2])
        self.owned_item.occasion.set([self.occasion1, self.occasion2])

    def setUp(self):
        super().setUp()
        self.post_setUp()

    def test_get_owned_item_authenticated(self):
        url = reverse('ownedItem-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_owned_item_unauthenticated(self):
        self.client.force_authenticate(user=None, token=None)
        url = reverse('ownedItem-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_owned_item_authenticated(self):
        url = reverse('ownedItem-detail', args=[1])
        response = self.client.patch(url, {'score': 50})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_owned_item_unauthenticated(self):
        self.client.force_authenticate(user=None, token=None)
        url = reverse('ownedItem-detail', args=[1])
        response = self.client.patch(url, {'score': 50})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_owned_item_score_range(self):
        url = reverse('ownedItem-detail', args=[1])
        response = self.client.patch(url, {'score': 150})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_owned_item_authenticated(self):
        url = reverse('ownedItem-detail', args=[1])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_owned_item_unauthenticated(self):
        self.client.force_authenticate(user=None, token=None)
        url = reverse('ownedItem-detail', args=[1])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_owned_item_authenticated(self):
        url = reverse('ownedItem-list')
        response = self.client.post(url, {
            'name': 'test',
            'season': 'Spring',
            'image': SimpleUploadedFile(
                'test.jpg',
                content=self.image_content,
                content_type='image/jpeg'
            ),
            'color': 'test blue',
            'type': 1,
            'material': [1],
            'occasion': [1],
            'brand': 1,
            'is_public': True,
            'score': 100
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_owned_item_unauthenticated(self):
        self.client.force_authenticate(user=None, token=None)
        url = reverse('ownedItem-list')
        response = self.client.post(url, {
            'name': 'test',
            'season': 'Spring',
            'image': 'test.jpg',
            'color': 'test blue',
            'type': 1,
            'material': 1,
            'occasion': 1,
            'brand': 1,
            'is_public': True,
            'score': 100
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_owned_item_detail_authenticated(self):
        url = reverse('ownedItem-detail', args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_owned_item_detail_unauthenticated(self):
        self.client.force_authenticate(user=None, token=None)
        url = reverse('ownedItem-detail', args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class OwnedItemByPKViewTest(CustomTestCase):

    def test_get_owned_item_by_pk_authenticated(self):
        url = reverse('ownedItemByPK-detail', args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_owned_item_by_pk_unauthenticated(self):
        self.client.force_authenticate(user=None, token=None)
        url = reverse('ownedItemByPK-detail', args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PublicItemViewTest(CustomTestCase):

    def setUp(self):
        super().setUp()
        OwnedItemViewTest.post_setUp(self)

    def test_get_public_item_authenticated(self):
        url = reverse('publicItem-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_public_item_unauthenticated(self):
        self.client.force_authenticate(user=None, token=None)
        url = reverse('publicItem-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_public_item_detail_authenticated(self):
        url = reverse('publicItem-detail', args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_public_item_detail_unauthenticated(self):
        self.client.force_authenticate(user=None, token=None)
        url = reverse('publicItem-detail', args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
