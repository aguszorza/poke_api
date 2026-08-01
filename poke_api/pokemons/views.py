from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from pokemons.poke_api_client import PokeApi
from pokemons.serializers import PokemonListSerializer, PokemonSerializer


@extend_schema(
    responses=PokemonListSerializer,
    description="Returns the list of pokemons that belongs to your types",
)
class PokemonListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_types = request.user.types
        pokemons = set()
        for pokemon_type in user_types:
            pokemons = pokemons.union(PokeApi.get_pokemons_from_type(pokemon_type))
        pokemons = [pokemon.data for pokemon in pokemons]
        return Response({"pokemons": pokemons})


@extend_schema(
    responses=PokemonSerializer,
    description="Given the pokemon id or name, returns its data if it belongs to your type",
)
class PokemonGetView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pokemon_key):
        user_types = request.user.types
        pokemon_details = PokeApi.get_pokemon_details(pokemon_key)
        not_found_response = Response(
            {"error": f"Pokemon {pokemon_key} Not Found"}, status=status.HTTP_404_NOT_FOUND
        )
        if pokemon_details is None:
            return not_found_response

        pokemon_details = pokemon_details.data
        pokemon_types = [pokemon_type["name"] for pokemon_type in pokemon_details["types"]]
        if len(set(user_types).intersection(pokemon_types)) == 0:
            return not_found_response

        return Response(pokemon_details)
