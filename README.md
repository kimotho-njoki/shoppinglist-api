[![Build Status](https://travis-ci.org/kimotho-njoki/shoppinglist-api.svg?branch=master)](https://travis-ci.org/kimotho-njoki/shoppinglist-api)

# Shoppinglist Api
Flask API for a shopping list application.
The ShoppingList application enables users to create accounts that enable them to Log In and create their own shopping lists as well as add items. 

## Getting Started
#### Clone the repository
> https://github.com/kimotho-njoki/shoppinglist-api

#### Navigate to the shoppinglist-api directory
>cd shoppinglist-api

#### Create and activate a virtual environment
>mkvirtualenv shoppinglist-api <br>
 workon shoppinglist-api

#### Requirements
Install all dependencies using
>pip install -r requirements.txt

#### Initialize, migrate and update the database
>python manage.py db init <br>
 python manage.py db migrate <br>
 python manage.py db upgrade <br>

#### Testing the application
>python manage.py test

#### Running the application
First set the environment variables
>set FLASK_APP=run.py <br>
 set SECRET=my_secret_random_key <br>
 set APP_SETTINGS=development <br>
 set DATABASE_URL=postgresql://postgres-user:password@localhost/dbname <br>

Then run the application
>python run.py

#### Application End points

| Resource URL | Method | Description | Requires Token |
| -------------|--------|-------------|----------------|
|/auth/register| POST   | User registration | FALSE |
|/auth/login   | POST   | User login   | FALSE |
|/shoppinglists/| POST | Create shoppinglist | TRUE |
|/shoppinglists/| GET  | Get all shoppinglists | TRUE |
|/shoppinglists/<int:list_id>| GET | Get shoppinglist by id | TRUE |
|/shoppinglists/<int:list_id>| PUT | Edit shoppinglist | TRUE |
|/shoppinglists/<int:list_id>| DELETE | Delete shoppinglist | TRUE |
|/shoppinglists/<int:list_id>/items | POST | Create an item | TRUE |
|/shoppinglists/<int:list_id>/items | GET  | Get all items | TRUE |
|/shoppinglists/<int:list_id>/items/<int:item_id> | GET | Get item by id | TRUE |
|/shoppinglists/<int:list_id>/items/<int:item_id> | PUT | Edit item | TRUE |
|/shoppinglists/<int:list_id>/items/<int:item_id> | DELETE | Delete item | TRUE |




