[![Build Status](https://travis-ci.org/kimotho-njoki/shoppinglist-api.svg?branch=master)](https://travis-ci.org/kimotho-njoki/shoppinglist-api) [![Coverage Status](https://coveralls.io/repos/github/kimotho-njoki/shoppinglist-api/badge.svg?branch=master)](https://coveralls.io/github/kimotho-njoki/shoppinglist-api?branch=master) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/39fc5b1359254b3caf273d1d2e038bbe)](https://www.codacy.com/app/kimotho-njoki/shoppinglist-api?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=kimotho-njoki/shoppinglist-api&amp;utm_campaign=Badge_Grade) [![Codacy Badge](https://api.codacy.com/project/badge/Coverage/39fc5b1359254b3caf273d1d2e038bbe)](https://www.codacy.com/app/kimotho-njoki/shoppinglist-api?utm_source=github.com&utm_medium=referral&utm_content=kimotho-njoki/shoppinglist-api&utm_campaign=Badge_Coverage)

# Shoppinglist Api
Flask API for a shopping list application.
The ShoppingList application enables users to create accounts that enable them to Log In and create their own shopping lists as well as add items. 

## Documentation
The documentation of this API can be found at:
> http://docs.shoppinglistapi6.apiary.io/#

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




