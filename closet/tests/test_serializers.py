# import essential modules
from django.conf import settings
from django.test import TestCase
from django.contrib.auth import get_user_model
from closet import models, serializers

import os


class SerializerTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@email.com',
            password='testpass123',
            first_name='test',
            last_name='user',
            phone_number='1234567890'
        )
        self.image_content = open(os.path.join(settings.MEDIA_ROOT, 'ItemPics/download.jpg'), 'rb').read()

        self.type = models.Type.objects.create(name='test type')
        self.brand = models.Brand.objects.create(name='test brand')
        self.material1 = models.Material.objects.create(name='test material 1')
        self.material2 = models.Material.objects.create(name='test material 2')
        self.occasion1 = models.Occasion.objects.create(name='test occasion 1')
        self.occasion2 = models.Occasion.objects.create(name='test occasion 2')

        self.owned_item = models.Item.objects.create(
            name='test',
            season='test season',
            image='test.jpg',
            color='test color',
            type=self.type,
            brand=self.brand,
        )

        self.owned_item.material.set([self.material1, self.material2])
        self.owned_item.occasion.set([self.occasion1, self.occasion2])

    def test_item_serializer(self):
        serializer = serializers.ItemSerializer(self.owned_item)
        self.assertEqual(serializer.data['name'], 'test')
        self.assertEqual(serializer.data['season'], 'test season')
        self.assertEqual(serializer.data['image'], '/media/test.jpg')
        self.assertEqual(serializer.data['color'], 'test color')
        self.assertEqual(serializer.data['typename'], 'test type')
        self.assertEqual(serializer.data['brandname'], 'test brand')
        self.assertEqual(serializer.data['materials'], ['test material 1', 'test material 2'])
        self.assertEqual(serializer.data['occasions'], ['test occasion 1', 'test occasion 2'])
        self.assertEqual(serializer.data['type'], self.type.id)
        self.assertEqual(serializer.data['brand'], self.brand.id)
        self.assertEqual(serializer.data['material'], [self.material1.id, self.material2.id])
        self.assertEqual(serializer.data['occasion'], [self.occasion1.id, self.occasion2.id])