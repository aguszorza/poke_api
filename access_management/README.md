# Access Management API

This API has the access management logic of the Poke API. The API will allow you to:

* Login
* Add a user to a group
* Remove a user from a group
* Obtain information of the current user and all the groups he belongs to

# Intallation

```bash
# Create your virtual environment
python -m venv venv
source venv/bin/activate

# install dependencies
pip install -r requirements.txt

# run migrations
python manage.py migrate

# create a superuser
python manage.py createsuperuser

# Populate with pokemon types
python manage.py create_pokemon_types

# Run application
python manage.py runserver 8000

# Test login
curl -X POST "http://localhost:8000/api/login/" -b '{"username": "your_user", "password": "your_password"}'

# Add user to group 'fire'
curl -X POST "http://localhost:8000/api/group/fire/add/" -H "Authorization: Bearer <your_token>"

# Remove user from fire group
curl -X POST "http://localhost:8000/api/group/fire/remove/" -H "Authorization: Bearer <your_token>"

# Obtain user information
curl -X GET "http://localhost:8000/api/user/me/" -H "Authorization: Bearer <your_token>"
```
