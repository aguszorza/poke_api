from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from pokemons.models import Pokemon


def format_pokemon(pokemon: Pokemon) -> dict:
    pokemon_types = [pokemon_type.name for pokemon_type in pokemon.types.all()]
    return {
        "id": pokemon.id,
        "name": pokemon.name,
        "types": pokemon_types
    }


class PokemonListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_types = request.user.types
        pokemons = Pokemon.objects.filter(types__name__in=user_types).distinct()
        return Response({"pokemons": [format_pokemon(pokemon) for pokemon in pokemons]})
