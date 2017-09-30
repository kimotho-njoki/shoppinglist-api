[![Build Status](https://travis-ci.org/kimotho-njoki/shoppinglist-api.svg?branch=master)](https://travis-ci.org/kimotho-njoki/shoppinglist-api)

# Shoppinglist Api
Flask API for a shopping list application.
The ShoppingList application enables users to create accounts that enable them to Log In and create their own shopping lists as well as add items. 

## Getting Started
Clone the repository
> https://github.com/kimotho-njoki/shoppinglist-api

####Navigate to the shoppinglist-api directory
>cd shoppinglist-api

####Create and activate a virtual environment
>mkvirtualenv shoppinglist-api
workon shoppinglist-api

####Requirements
Install all dependencies using
>pip install -r requirements.txt

####Initialize, migrate and update the database
>python manage.py db init
python manage.py db migrate
python manage.py db upgrade

####Testing the application
>python manage.py test

####Running the application
First set the environment variables
>set FLASK_APP=run.py 
set SECRET=my_secret_random_key 
set APP_SETTINGS=development
set DATABASE_URL=postgresql://postgres-user:password@localhost/dbname

Then run the application
>python run.py

####Application End points

| Resource URL | Method | Description | Requires Token |
| -------------|--------|-------------|----------------|
|/auth/register| POST   | User registration | FALSE |
|/auth/login   | POST   | User login   | FALSE |
|/shoppinglists/| POST | Create shoppinglist | TRUE |
|/shoppinglists/| GET  | Get all shoppinglists | TRUE |
|/shoppinglists/<int:list_id>| GET | Get shoppinglist by id | True |
|/shoppinglists/<int:list_id>| PUT | Edit shoppinglist | True |
|/shoppinglists/<int:list_id>| DELETE | Delete shoppinglist | True |
|/shoppinglists/<int:list_id>/items | POST | Create an item | True |
|/shoppinglists/<int:list_id>/items | GET  | Get all items | True |
|/shoppinglists/<int:list_id>/items/<int:item_id> | GET | Get item by id | True |
|/shoppinglists/<int:list_id>/items/<int:item_id> | PUT | Edit item | True |
|/shoppinglists/<int:list_id>/items/<int:item_id> | DELETE | Delete item | True |




