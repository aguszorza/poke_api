from rest_framework import serializers

from django.contrib.auth.models import User


class LoginInputSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class UserSerializer(serializers.ModelSerializer):

    types = serializers.SlugRelatedField(
        source="groups",
        many=True,
        read_only=True,
        slug_field="name",
    )

    class Meta:
        model = User
        fields = ["id", "username", "email", "types"]
