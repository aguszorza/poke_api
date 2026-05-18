import pytest

from django.core.management import call_command

from pokemons.management.commands.create_pokemon_types import pokemon_types
from pokemons.management.commands.create_pokemons import pokemons
from pokemons.models import Pokemon, PokemonType


@pytest.mark.django_db
def test_create_pokemon_types():

    call_command("create_pokemon_types")

    assert PokemonType.objects.count() == len(pokemon_types)


@pytest.mark.django_db
def test_create_pokemons():

    call_command("create_pokemons")

    assert Pokemon.objects.count() == len(pokemons)
