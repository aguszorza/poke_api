import pytest

from rest_framework import status


@pytest.mark.unit
class TestProtectedEndpoint:
    def test_get_authenticated(self, authenticated_client, mock_auth_api):
        response = authenticated_client.get("/api/protected/")

        assert response.status_code == status.HTTP_200_OK

        assert "message" in response.data
        assert "user_id" in response.data
        assert "username" in response.data

    def test_get_unauthenticated(self, api_client):
        response = api_client.get("/api/protected/")

        assert response.status_code == status.HTTP_403_FORBIDDEN
