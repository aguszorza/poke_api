from django.db import models


class PokemonType(models.Model):
    class Meta:
        db_table = "pokemon_type"

    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Pokemon(models.Model):
    name = models.CharField(max_length=100, unique=True)
    types = models.ManyToManyField(
        PokemonType,
        related_name="pokemons",
        blank=True,
    )

    def __str__(self):
        return self.name
