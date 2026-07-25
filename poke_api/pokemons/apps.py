from django.apps import AppConfig


class PokemonsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "pokemons"

    def ready(self):
        import authentication.schema  # noqa: F401
