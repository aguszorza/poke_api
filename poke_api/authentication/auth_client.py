import requests

from django.conf import settings


AUTH_API_BASE_URL = settings.CONFIG.AUTH_API_BASE_URL


class AuthApiClient:
    @staticmethod
    def get_current_user(token):

        response = requests.get(
            f"{AUTH_API_BASE_URL}/user/me/",
            headers={
                "Authorization": token
            },
            timeout=5
        )

        if response.status_code != 200:
            return None

        return response.json()
