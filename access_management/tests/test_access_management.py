import pytest

from rest_framework import status


@pytest.mark.unit
class TestUserMe:
    def test_get_profile_authenticated(self, authenticated_client):
        response = authenticated_client.get("/api/user/me/")

        assert response.status_code == status.HTTP_200_OK

        assert "id" in response.data
        assert "username" in response.data
        assert "email" in response.data


    def test_get_profile_unauthenticated(self, api_client):
        response = api_client.get("/api/user/me/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
