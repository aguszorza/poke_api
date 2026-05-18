# Poke API

This API has the information of the pokemons. The API will allow you to:

* Return the list of pokemons you have acces to
* Return the one pokemon you have acces to

# Intallation

```bash
# Create your virtual environment
python -m venv venv
source venv/bin/activate

# install app dependencies
pip install .

# install app dependencies for development
pip install -e .[test]


# run migrations
python manage.py migrate

# Populate with pokemon types
python manage.py create_pokemon_types

# Populate with some pokemons
python manage.py create_pokemons

# Run application
python manage.py runserver 8001
```
