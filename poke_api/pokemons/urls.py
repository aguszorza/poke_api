from django.urls import path
from pokemons.views import PokemonListView

urlpatterns = [
    path('pokemon/', PokemonListView.as_view(), name='pokemons'),
]
