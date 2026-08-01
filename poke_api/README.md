# Poke API

This API will search for the pokemons information in POKE API if the user has permissions to do it. The API will allow you to:

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

# create a .env file using the .env.test as example

# Run application
python manage.py runserver 8001

# Access to swagger from
http://localhost:8001/api/docs/
```
