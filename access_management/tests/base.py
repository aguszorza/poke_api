from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken


User = get_user_model()


class BaseAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )

    def authenticate(self, user=None):
        """
        Authenticate requests with JWT token.
        """
        user = user or self.user

        refresh = RefreshToken.for_user(user)

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}"
        )

        return user

    def assertStatus(self, response, status_code):
        self.assertEqual(response.status_code, status_code)

    def assertHasKeys(self, data, keys):
        for key in keys:
            self.assertIn(key, data)
