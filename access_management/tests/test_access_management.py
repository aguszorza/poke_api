from django.contrib.auth.models import Group
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


@pytest.mark.unit
class TestAddGroup:
    def test_add_unknown_group(self, authenticated_client):
        response = authenticated_client.post("/api/group/unknown/add/")

        assert response.status_code == status.HTTP_404_NOT_FOUND

        assert "error" in response.data
        assert response.data == {"error": "Group unknown Not Found"}

    def test_add_to_existing_group(self, authenticated_client):
        Group.objects.create(name='water')

        response = authenticated_client.post("/api/group/water/add/")

        assert response.status_code == status.HTTP_200_OK
        assert "types" in response.data
        assert response.data["types"] == ["water"]
    
    def test_add_multiple_times_to_same_group(self, authenticated_client):
        Group.objects.create(name='water')

        responses = [
            authenticated_client.post("/api/group/water/add/"),
            authenticated_client.post("/api/group/water/add/"),
            authenticated_client.post("/api/group/water/add/"),
        ]


        assert all([response.status_code == status.HTTP_200_OK for response in responses]) is True
        assert responses[-1].data["types"] == ["water"]
        assert [group.name for group in Group.objects.all()] == ["water"]

    def test_add_to_multiple_groups(self, authenticated_client):
        Group.objects.create(name='water')
        Group.objects.create(name='fire')
        Group.objects.create(name='earth')

        responses = [
            authenticated_client.post("/api/group/water/add/"),
            authenticated_client.post("/api/group/fire/add/"),
            authenticated_client.post("/api/group/earth/add/"),
        ]


        assert all([response.status_code == status.HTTP_200_OK for response in responses]) is True
        assert responses[-1].data["types"] == ["water", "fire", "earth"]

    def test_add_group_unauthenticated(self, api_client):
        response = api_client.post("/api/group/water/add/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
