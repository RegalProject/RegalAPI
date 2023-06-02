from django.test import TestCase
from django.contrib.auth import get_user_model
from closet import models, serializers


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

    def test_crawled_item_serializer(self):
        crawled_item = models.CrawledItem.objects.create(
            name='test',
            season='test season',
            image='test.jpg',
            color='test color',
            type=self.type,
            brand=self.brand,
            price=10000,
            url='https://testurl.com'
        )

        crawled_item.material.set([self.material1, self.material2])
        crawled_item.occasion.set([self.occasion1, self.occasion2])

        serializer = serializers.CrawledItemSerializer(crawled_item)
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
        self.assertEqual(serializer.data['price'], 10000)
        self.assertEqual(serializer.data['url'], 'https://testurl.com')

    def test_owned_item_serializer(self):
        owned_item = models.OwnedItem.objects.create(
            name='test',
            season='test season',
            image='test.jpg',
            color='test color',
            type=self.type,
            brand=self.brand,
            owner=self.user,
            score=76,
            is_public=True
        )

        owned_item.material.set([self.material1, self.material2])
        owned_item.occasion.set([self.occasion1, self.occasion2])

        serializer = serializers.OwnedItemSerializer(owned_item, required=False)
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
        self.assertEqual(serializer.data['score'], 76)
        self.assertEqual(serializer.data['is_public'], True)

    def test_brand_serializer(self):
        serializer = serializers.BrandSerializer(self.brand)
        self.assertEqual(serializer.data['name'], 'test brand')

    def test_material_serializer(self):
        serializer = serializers.MaterialSerializer(self.material1)
        self.assertEqual(serializer.data['name'], 'test material 1')

    def test_occasion_serializer(self):
        serializer = serializers.OccasionSerializer(self.occasion1)
        self.assertEqual(serializer.data['name'], 'test occasion 1')

    def test_type_serializer(self):
        serializer = serializers.TypeSerializer(self.type)
        self.assertEqual(serializer.data['name'], 'test type')
