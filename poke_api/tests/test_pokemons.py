import pytest
from rest_framework import status

from pokemons.models import Pokemon, PokemonType


@pytest.mark.unit
@pytest.mark.django_db
class TestListPokemonEndpoint:
    @pytest.fixture(autouse=True)
    def setup_method(self):
        self.fire = PokemonType.objects.create(name="fire")
        self.flying = PokemonType.objects.create(name="flying")
        self.first_pokemon = Pokemon.objects.create(name="charizard")
        self.second_pokemon = Pokemon.objects.create(name="bird")
        self.first_pokemon.types.set([self.fire, self.flying])
        self.second_pokemon.types.set([self.flying])

    def test_get_pokemons_user_with_no_types(self, authenticated_client, mock_auth_api):
        response = authenticated_client.get("/api/pokemon/")

        assert response.status_code == status.HTTP_200_OK

        assert "pokemons" in response.data
        assert response.data["pokemons"] == []

    def test_get_pokemons_user_with_one_type(self, authenticated_client, mock_auth_api):
        mock_auth_api(
            {
                "id": 1,
                "email": "john@example.com",
                "username": "john",
                "types": ["fire"]
            }
        )
        response = authenticated_client.get("/api/pokemon/")

        assert response.status_code == status.HTTP_200_OK

        assert "pokemons" in response.data
        assert len(response.data["pokemons"]) == 1
        assert response.data["pokemons"][0]["name"] == self.first_pokemon.name
    
    def test_get_pokemons_with_shared_type(self, authenticated_client, mock_auth_api):
        mock_auth_api(
            {
                "id": 1,
                "email": "john@example.com",
                "username": "john",
                "types": ["fire", "flying"]
            }
        )
        response = authenticated_client.get("/api/pokemon/")

        assert response.status_code == status.HTTP_200_OK

        assert "pokemons" in response.data
        assert len(response.data["pokemons"]) == 2  # Charizard is not repeated
        pokemon_names = [pokemon["name"] for pokemon in response.data["pokemons"]]
        assert self.first_pokemon.name in pokemon_names
        assert self.second_pokemon.name in pokemon_names

    def test_get_unauthenticated(self, api_client):
        response = api_client.get("/api/pokemon/")

        # TODO: check why it returns 403 instead of 401
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.unit
@pytest.mark.django_db
class TestGetPokemonEndpoint:
    @pytest.fixture(autouse=True)
    def setup_method(self):
        self.fire = PokemonType.objects.create(name="fire")
        self.flying = PokemonType.objects.create(name="flying")
        self.pokemon = Pokemon.objects.create(name="charizard")
        self.pokemon.types.set([self.fire, self.flying])

    def test_get_pokemon_user_with_no_types(self, authenticated_client, mock_auth_api):
        response = authenticated_client.get("/api/pokemon/charizard/")

        assert response.status_code == status.HTTP_404_NOT_FOUND

        assert "error" in response.data
        assert response.data["error"] == "Pokemon charizard Not Found"

    def test_get_pokemon_by_name(self, authenticated_client, mock_auth_api):
        mock_auth_api(
            {
                "id": 1,
                "email": "john@example.com",
                "username": "john",
                "types": ["fire"]
            }
        )
        response = authenticated_client.get("/api/pokemon/charizard/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == self.pokemon.name
    
    def test_get_pokemon_by_id(self, authenticated_client, mock_auth_api):
        mock_auth_api(
            {
                "id": 1,
                "email": "john@example.com",
                "username": "john",
                "types": ["fire"]
            }
        )
        response = authenticated_client.get(f"/api/pokemon/{self.pokemon.id}/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == self.pokemon.name

    def test_get_pokemon_having_both_types(self, authenticated_client, mock_auth_api):
        mock_auth_api(
            {
                "id": 1,
                "email": "john@example.com",
                "username": "john",
                "types": ["fire", "flying"]
            }
        )
        response = authenticated_client.get("/api/pokemon/charizard/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == self.pokemon.name

    def test_get_unauthenticated(self, api_client):
        response = api_client.get("/api/pokemon/charizard/")

        # TODO: check why it returns 403 instead of 401
        assert response.status_code == status.HTTP_403_FORBIDDEN
