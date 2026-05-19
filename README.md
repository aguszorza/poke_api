# PokeAPI project

Simple project composed by two APIs. The access management API that will manage users and the types they belong to, and the Poke API that will return the pokemons that belongs to the types of the user


# Run Access Management API

Please follow the installation instructions from the [README](./access_management/README.md#Intallation). Then run the API with `python manage.py runserver 8000`


# Run Poke API

Please follow the installation instructions from the [README](./poke_api/README.md#Intallation). Then run the API with `python manage.py runserver 8001`

# Execute endpoints

You can execute each endpoint using curl or you can access to their swagger documentation. Each API has an endpoint to access to the API documentation that shows all available endpoints and allows you to test them. The endpoint is `/api/docs/`. If you followed the documentation the API documentation should be available in the following URLs:

* Access Management API: http://localhost:8000/api/docs/
* Poke API: http://localhost:8001/api/docs/
