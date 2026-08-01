from urllib.parse import urlparse

from rest_framework import serializers


def get_id_from_url(url: str) -> int:
    if not url:
        return None

    path = urlparse(url).path.rstrip("/")
    return int(path.split("/")[-1])


class TypesSerializer(serializers.Serializer):
    id = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    def get_name(self, obj):
        type_details = obj.get("type", {})
        return type_details.get("name", "")

    def get_id(self, obj):
        type_details = obj.get("type", {})
        url = type_details.get("url")
        return get_id_from_url(url)


class PokemonDetailsSerializer(serializers.Serializer):
    name = serializers.CharField()
    id = serializers.IntegerField()
    weight = serializers.IntegerField()
    height = serializers.IntegerField()
    types = TypesSerializer(many=True)


class PokemonSerializer(serializers.Serializer):
    name = serializers.CharField()
    id = serializers.SerializerMethodField()

    def get_id(self, obj):
        url = obj.get("url")
        return get_id_from_url(url)

    def __hash__(self):
        return hash(self.data["id"])

    def __eq__(self, other):
        if not isinstance(other, PokemonSerializer):
            return NotImplemented
        return self.data["id"] == other.data["id"]


class PokemonListSerializer(serializers.Serializer):
    pokemons = PokemonSerializer(
        many=True,
    )
