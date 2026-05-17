from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

# obtained from https://pokeapi.co/api/v2/type
pokemon_types = ['normal', 'fighting', 'flying', 'poison', 'ground', 'rock', 'bug', 'ghost', 'steel', 'fire', 'water', 'grass', 'electric', 'psychic', 'ice', 'dragon', 'dark', 'fairy', 'stellar', 'unknown', 'shadow']


class Command(BaseCommand):
    help = "Create all pokemon type groups"

    def handle(self, *args, **kwargs):
        for pokemon_type in pokemon_types:
            _, created = Group.objects.get_or_create(name=pokemon_type)

            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"Created group: {pokemon_type}")
                )
            else:
                self.stdout.write(f"Group already exists: {pokemon_type}")
