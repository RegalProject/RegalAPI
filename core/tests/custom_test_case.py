from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from core.models import Profile


class CustomTestCase(APITestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='test',
            password='password123',
            first_name='test',
            last_name='test',
            phone_number='09123456789',
            email='test@test.com'
        )

        self.profile = Profile.objects.get(user=self.user)

        self.refresh_token = RefreshToken.for_user(self.user)
        self.access_token = AccessToken.for_user(self.user)
        # print(self.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'JWT {self.access_token}')

    def tearDown(self):
        pass

