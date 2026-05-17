from django.contrib.auth.models import Group, User
import pytest

from rest_framework import status


@pytest.mark.unit
class TestLogin:
    def test_login_invalid_credentials(self, authenticated_client):
        current_user = User.objects.first()
        data = {
            "username": current_user.username,
            "password": "fake_invalid"
        }

        response = authenticated_client.post("/api/login/", data=data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_login_valid_credentials(self, authenticated_client):
        username = "my_user"
        fake_password = "fake_password"
        user = User.objects.create(username=username, email="my_user@mail.com")
        user.set_password(fake_password)
        user.save()
        data = {
            "username": username,
            "password": fake_password
        }

        response = authenticated_client.post("/api/login/", data=data)

        assert response.status_code == status.HTTP_200_OK
        assert "access_token" in response.data
        assert "refresh_token" in response.data


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
class TestAddToGroup:
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


@pytest.mark.unit
class TestRemoveFromGroup:
    def test_remove_from_unknown_group_works(self, authenticated_client):
        response = authenticated_client.post("/api/group/unknown/remove/")

        assert response.status_code == status.HTTP_204_NO_CONTENT

        assert response.data is None

    def test_remove_from_existing_group_removes_group(self, authenticated_client):
        water_type = Group.objects.create(name='water')
        fire_type = Group.objects.create(name='fire')
        current_user  = User.objects.first()
        current_user.groups.add(water_type)
        current_user.groups.add(fire_type)
        assert current_user.groups.contains(fire_type) is True
        assert current_user.groups.contains(water_type) is True

        response = authenticated_client.post("/api/group/water/remove/")

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert response.data is None
        assert current_user.groups.contains(fire_type) is True
        assert current_user.groups.contains(water_type) is False
    
    def test_remove_multiple_times_from_same_group(self, authenticated_client):
        water_type = Group.objects.create(name='water')
        fire_type = Group.objects.create(name='fire')
        current_user  = User.objects.first()
        current_user.groups.add(water_type)
        current_user.groups.add(fire_type)
        assert current_user.groups.contains(fire_type) is True
        assert current_user.groups.contains(water_type) is True

        responses = [
            authenticated_client.post("/api/group/water/remove/"),
            authenticated_client.post("/api/group/water/remove/"),
            authenticated_client.post("/api/group/water/remove/"),
        ]


        assert all([response.status_code == status.HTTP_204_NO_CONTENT for response in responses]) is True
        assert current_user.groups.contains(fire_type) is True
        assert current_user.groups.contains(water_type) is False

    def test_remove_from_multiple_groups(self, authenticated_client):
        water_type = Group.objects.create(name='water')
        fire_type = Group.objects.create(name='fire')
        earth_type = Group.objects.create(name='earth')
        current_user  = User.objects.first()
        current_user.groups.add(water_type)
        current_user.groups.add(fire_type)
        current_user.groups.add(earth_type)

        responses = [
            authenticated_client.post("/api/group/water/remove/"),
            authenticated_client.post("/api/group/fire/remove/"),
        ]


        assert all([response.status_code == status.HTTP_204_NO_CONTENT for response in responses]) is True
        assert current_user.groups.contains(fire_type) is False
        assert current_user.groups.contains(water_type) is False
        assert current_user.groups.contains(earth_type) is True

    def test_remove_from_group_unauthenticated(self, api_client):
        response = api_client.post("/api/group/water/remove/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
