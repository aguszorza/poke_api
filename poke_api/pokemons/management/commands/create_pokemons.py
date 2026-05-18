from django.core.management.base import BaseCommand
from pokemons.models import Pokemon, PokemonType

# obtained from https://pokeapi.co/api/v2/pokemon/<name>
pokemons = [
    {"name": "ditto", "types": ["normal"]},
    {"name": "charizard", "types": ["fire", "flying"]},
    {"name": "eevee", "types": ["normal"]},
    {"name": "squirtle", "types": ["water"]},
    {"name": "psyduck", "types": ["water"]},
    {"name": "golduck", "types": ["water"]},
    {"name": "beedrill", "types": ["bug", "poison"]},
    {"name": "pidgeotto", "types": ["normal", "flying"]},
    {"name": "alakazam", "types": ["psychic"]},
]


class Command(BaseCommand):
    help = "Create some pokemons"

    def handle(self, *args, **kwargs):
        for pokemon in pokemons:
            pokemon_name = pokemon["name"]
            pokemon_types = PokemonType.objects.filter(name__in=pokemon["types"]).all()
            pokemon, created = Pokemon.objects.get_or_create(name=pokemon_name)
            pokemon.types.set(pokemon_types)

            if created:
                self.stdout.write(self.style.SUCCESS(f"Created group: {pokemon_name}"))
            else:
                self.stdout.write(f"Pokemon already exists: {pokemon_name}")
