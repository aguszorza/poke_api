from django.conf import settings
import requests
from typing import Optional

from pokemons.serializers import PokemonDetailsSerializer, PokemonSerializer

POKE_API_BASE_URL = settings.CONFIG.POKE_API_BASE_URL


class PokeApi:
    @staticmethod
    def get_pokemons_from_type(pokemon_type: str) -> list[PokemonSerializer]:
        url = f"{POKE_API_BASE_URL}/type/{pokemon_type}"

        response = requests.get(url, timeout=5)

        if response.status_code != 200:
            return []

        data = response.json()
        pokemons = data.get("pokemon", [])
        pokemons = [PokemonSerializer(pokemon["pokemon"]) for pokemon in pokemons]
        return pokemons

    @staticmethod
    def get_pokemon_details(pokemon_identifier: str) -> Optional[PokemonDetailsSerializer]:
        """Returns the pokemon details
        Args:
            pokemon_identifier (str): pokemon name or id
        """
        url = f"{POKE_API_BASE_URL}/pokemon/{pokemon_identifier}"

        response = requests.get(url, timeout=5)

        if response.status_code != 200:
            return None

        return PokemonDetailsSerializer(response.json())
