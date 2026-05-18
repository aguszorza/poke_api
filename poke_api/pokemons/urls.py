from django.urls import path
from pokemons.views import PokemonGetView, PokemonListView

urlpatterns = [
    path("pokemon/", PokemonListView.as_view(), name="pokemons"),
    path("pokemon/<str:pokemon_key>/", PokemonGetView.as_view()),
]
