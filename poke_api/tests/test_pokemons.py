import pytest
from rest_framework import status
from unittest.mock import Mock, patch


def pokemon_details_to_poke_api_list(pokemons: list[dict]):
    pokemons = [
        {
            "pokemon": {
                "name": pokemon["name"],
                "url": f"https://pokeapi.co/api/v2/type/{pokemon['id']}/",
            }
        }
        for pokemon in pokemons
    ]
    return {"pokemon": pokemons}


def pokemon_details_to_poke_api_details(pokemon: dict):
    pokemon_types = [
        {
            "type": {
                "name": pokemon_type["name"],
                "url": f"https://pokeapi.co/api/v2/type/{pokemon_type['id']}/",
            }
        }
        for pokemon_type in pokemon["types"]
    ]
    return {
        "id": pokemon["id"],
        "name": pokemon["name"],
        "types": pokemon_types,
        "height": 10,
        "weight": 45,
    }


@pytest.mark.unit
class TestListPokemonEndpoint:
    @pytest.fixture(autouse=True)
    def setup_method(self):
        self.first_pokemon = {
            "id": 1,
            "name": "charizard",
            "types": [{"name": "flying", "id": 1}, {"name": "fire", "id": 2}],
        }
        self.second_pokemon = {"id": 2, "name": "bird", "types": [{"name": "flying", "id": 1}]}

    def test_get_pokemons_user_with_no_types(self, authenticated_client, mock_auth_api):
        response = authenticated_client.get("/api/pokemon/")

        assert response.status_code == status.HTTP_200_OK

        assert "pokemons" in response.data
        assert response.data["pokemons"] == []

    def test_get_pokemons_user_with_one_type(self, authenticated_client, mock_auth_api):
        mock_auth_api({"id": 1, "email": "john@example.com", "username": "john", "types": ["fire"]})
        mock = Mock()
        response_mock = Mock()
        mock.get.return_value = response_mock
        response_mock.status_code = 200
        response_mock.json.return_value = pokemon_details_to_poke_api_list([self.first_pokemon])
        with patch("pokemons.poke_api_client.requests", mock):
            response = authenticated_client.get("/api/pokemon/")

        assert response.status_code == status.HTTP_200_OK

        assert "pokemons" in response.data
        assert len(response.data["pokemons"]) == 1
        assert response.data["pokemons"][0]["name"] == self.first_pokemon["name"]

    def test_get_pokemons_with_shared_type(self, authenticated_client, mock_auth_api):
        mock_auth_api(
            {"id": 1, "email": "john@example.com", "username": "john", "types": ["fire", "flying"]}
        )
        mock = Mock()
        response_mock = Mock()
        mock.get.return_value = response_mock
        response_mock.status_code = 200
        response_mock.json.side_effect = [
            pokemon_details_to_poke_api_list([self.first_pokemon]),
            pokemon_details_to_poke_api_list([self.first_pokemon, self.second_pokemon]),
        ]
        with patch("pokemons.poke_api_client.requests", mock):
            response = authenticated_client.get("/api/pokemon/")

        assert response.status_code == status.HTTP_200_OK

        assert "pokemons" in response.data
        assert len(response.data["pokemons"]) == 2  # Charizard is not repeated
        pokemon_names = [pokemon["name"] for pokemon in response.data["pokemons"]]
        assert self.first_pokemon["name"] in pokemon_names
        assert self.second_pokemon["name"] in pokemon_names

    def test_get_unauthenticated(self, api_client):
        response = api_client.get("/api/pokemon/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.unit
@pytest.mark.django_db
class TestGetPokemonEndpoint:
    @pytest.fixture(autouse=True)
    def setup_method(self):
        self.pokemon = {
            "id": 1,
            "name": "charizard",
            "types": [{"name": "flying", "id": 1}, {"name": "fire", "id": 2}],
        }

    def test_get_pokemon_user_with_no_types(self, authenticated_client, mock_auth_api):
        mock = Mock()
        response_mock = Mock()
        mock.get.return_value = response_mock
        response_mock.status_code = 200
        response_mock.json.return_value = pokemon_details_to_poke_api_details(self.pokemon)
        with patch("pokemons.poke_api_client.requests", mock):
            response = authenticated_client.get("/api/pokemon/charizard/")

        assert response.status_code == status.HTTP_404_NOT_FOUND

        assert "error" in response.data
        assert response.data["error"] == "Pokemon charizard Not Found"

    def test_get_unknown_pokemon(self, authenticated_client, mock_auth_api):
        mock_auth_api({"id": 1, "email": "john@example.com", "username": "john", "types": ["fire"]})
        mock = Mock()
        response_mock = Mock()
        mock.get.return_value = response_mock
        response_mock.status_code = 404
        with patch("pokemons.poke_api_client.requests", mock):
            response = authenticated_client.get("/api/pokemon/not_known/")

        assert response.status_code == status.HTTP_404_NOT_FOUND

        assert "error" in response.data
        assert response.data["error"] == "Pokemon not_known Not Found"

    def test_get_pokemon_by_name(self, authenticated_client, mock_auth_api):
        mock_auth_api({"id": 1, "email": "john@example.com", "username": "john", "types": ["fire"]})
        mock = Mock()
        response_mock = Mock()
        mock.get.return_value = response_mock
        response_mock.status_code = 200
        response_mock.json.return_value = pokemon_details_to_poke_api_details(self.pokemon)
        with patch("pokemons.poke_api_client.requests", mock):
            response = authenticated_client.get("/api/pokemon/charizard/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == self.pokemon["name"]

    def test_get_pokemon_by_id(self, authenticated_client, mock_auth_api):
        mock_auth_api({"id": 1, "email": "john@example.com", "username": "john", "types": ["fire"]})
        mock = Mock()
        response_mock = Mock()
        mock.get.return_value = response_mock
        response_mock.status_code = 200
        response_mock.json.return_value = pokemon_details_to_poke_api_details(self.pokemon)
        with patch("pokemons.poke_api_client.requests", mock):
            response = authenticated_client.get(f"/api/pokemon/{self.pokemon['id']}/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == self.pokemon["name"]

    def test_get_pokemon_having_both_types(self, authenticated_client, mock_auth_api):
        mock_auth_api(
            {"id": 1, "email": "john@example.com", "username": "john", "types": ["fire", "flying"]}
        )
        mock = Mock()
        response_mock = Mock()
        mock.get.return_value = response_mock
        response_mock.status_code = 200
        response_mock.json.return_value = pokemon_details_to_poke_api_details(self.pokemon)
        with patch("pokemons.poke_api_client.requests", mock):
            response = authenticated_client.get("/api/pokemon/charizard/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == self.pokemon["name"]

    def test_get_unauthenticated(self, api_client):
        response = api_client.get("/api/pokemon/charizard/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
