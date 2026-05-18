from django.core.management.base import BaseCommand
from pokemons.models import PokemonType

# obtained from https://pokeapi.co/api/v2/type
pokemon_types = [
    "normal",
    "fighting",
    "flying",
    "poison",
    "ground",
    "rock",
    "bug",
    "ghost",
    "steel",
    "fire",
    "water",
    "grass",
    "electric",
    "psychic",
    "ice",
    "dragon",
    "dark",
    "fairy",
    "stellar",
    "unknown",
    "shadow",
]


class Command(BaseCommand):
    help = "Create all pokemon type groups"

    def handle(self, *args, **kwargs):
        for pokemon_type in pokemon_types:
            _, created = PokemonType.objects.get_or_create(name=pokemon_type)

            if created:
                self.stdout.write(self.style.SUCCESS(f"Created pokemon type: {pokemon_type}"))
            else:
                self.stdout.write(f"Pokemon type already exists: {pokemon_type}")
