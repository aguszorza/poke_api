import pytest
import requests

from rest_framework.test import APIClient

FAKE_AUTH_HEADER = "Bearer 123456"


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_client(api_client):
    api_client.credentials(HTTP_AUTHORIZATION=FAKE_AUTH_HEADER)

    return api_client


class MockResponse:
    def __init__(self, status_code, data=None):
        self.status_code = status_code
        self._data = data or {}

    def json(self):
        return self._data


@pytest.fixture
def mock_auth_api(monkeypatch):
    response_data = {"id": 1, "email": "john@example.com", "username": "john", "types": []}

    def set_response(new_data):
        nonlocal response_data
        response_data = new_data

    def mock_get(url, headers=None, timeout=None):
        token = headers.get("Authorization")

        if token == FAKE_AUTH_HEADER:
            return MockResponse(200, response_data)
        raise requests.exceptions.HTTPError("Invalid token")

    monkeypatch.setattr(requests, "get", mock_get)

    return set_response
