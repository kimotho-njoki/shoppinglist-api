from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify, abort

from instance.config import app_config

db = SQLAlchemy()

def create_app(config_name):
	from app.models import User, ShoppingList
	app = FlaskAPI(__name__, instance_relative_config=True)
	app.config.from_object(app_config[config_name])
	app.config.from_pyfile('config.py')
	app.config['SQLALCHEMY_TRACK_MODIFICAIONS']=False
	#prepare application to work with SQLAlchemy
	db.init_app(app)

	@app.route('/shoppinglists/', methods=['POST', 'GET'])
	def shoppinglists():
		if request.method == 'POST':
			name = str(request.data.get('name', ''))
			if name:
				shoppinglist = ShoppingList(name=name)
				shoppinglist.save()
				response = jsonify({
					'id' : shoppinglist.id,
					'name' : shoppinglist.name,
					'date_created' : shoppinglist.date_created,
					'date_modified' : shoppinglist.date_modified
				})
				response.status_code = 201
				return response
		else:
			shoppinglists = ShoppingList.get_all()
			results = []

			for shoppinglist in shoppinglists:
				obj = {
				    'id' : shoppinglist.id,
				    'name' : shoppinglist.name,
				    'date_created' : shoppinglist.date_created,
				    'date_modified' : shoppinglist.date_modified
				}
				results.append(obj)
				response = jsonify(results)
				response.status_code = 200
				return response
	
	return app
