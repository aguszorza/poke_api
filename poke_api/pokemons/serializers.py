from rest_framework import serializers

from pokemons.models import Pokemon


class PokemonSerializer(serializers.ModelSerializer):

    types = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name",
    )

    class Meta:
        model = Pokemon
        fields = ["id", "name", "types"]


class PokemonListSerializer(serializers.Serializer):
    pokemons = PokemonSerializer(
        many=True,
    )
