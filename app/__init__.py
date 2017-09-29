from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify, abort, make_response

from instance.config import app_config

db = SQLAlchemy()

def create_app(config_name):
    from app.models import ShoppingList, User, ShoppingListItems
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICAIONS']=False
    # prepare application to work with SQLAlchemy
    db.init_app(app)

    @app.route('/shoppinglists/', methods=['POST', 'GET'])
    def shoppinglists():
        """
        Create and retrieve all shoppinglists
        """
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]

        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance (user_id, str):
                if request.method == 'POST':
                    name = str(request.data.get('name', ''))
                    if name:
                        shoppinglist = ShoppingList(name=name, user_id=user_id)
                        shoppinglist.save()
                        response = jsonify({
                            'id' : shoppinglist.id,
                            'name' : shoppinglist.name,
                            'date_created' : shoppinglist.date_created,
                            'date_modified' : shoppinglist.date_modified
                        })
                        return make_response(response), 201
                else:
                    shoppinglists = ShoppingList.get_all(user_id)
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
                    return make_response(response), 200
            else:
                message = user_id
                response = {
                'message' : message
                }
                return make_response(jsonify(response)), 401


    @app.route('/shoppinglists/<int:list_id>', methods=['GET'])
    def get_shoppinglist(user_id, list_id):
        """
        Get shoppinglist by id
        """
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]
        if access_token:
            user_id = User.decode_token(access_token)
            print user_id
            if not isinstance (user_id, str):
                shoppinglist = ShoppingList.query.filter_by(id=list_id, user_id=user_id).first()
                print shoppinglist
                if shoppinglist.user_id == user_id:
                    response = jsonify({
                        'id' : shoppinglist.id,
                        'name' : shoppinglist.name,
                        'date_created' : shoppinglist.date_created,
                        'date_modified' : shoppinglist.date_modified
                    })
                    response.status_code = 200
                    return response
                else:
                    abort(404)
            else:
                message = user_id
                response = {
                'message' : message
                }
                return make_response(jsonify(response)), 401

    @app.route('/shoppinglists/<int:list_id>', methods=['PUT'])
    def edit_shoppinglist(user_id, list_id):
        """
        Update a shopping list
        """
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]
        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance (user_id, str):
                shoppinglist = ShoppingList.query.filter_by(id=list_id, user_id=user_id).first()
                if not shoppinglist:
                    abort(404)
                if request.method == 'PUT':
                    name = str(request.data.get('name', ''))
                    shoppinglist.name = name
                    shoppinglist.save()
                    response = jsonify({
                        'id' : shoppinglist.id,
                        'name' : shoppinglist.name,
                        'date_created' : shoppinglist.date_created,
                        'date_modified' : shoppinglist.date_modified
                    })
                    response.status_code = 200
                    return response
            else:
                message = user_id
                response = {
                "message" : message
                }
                return make_response(jsonify(response)), 401

    @app.route('/shoppinglists/<int:list_id>', methods=['DELETE'])
    def delete_shoppinglist(user_id, list_id):
        """
        Delete a shopping list 
        """
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]
        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance (user_id, str):
                shoppinglist = ShoppingList.query.filter_by(id=list_id, user_id=user_id).first()
                if not shoppinglist:
                    abort(404)
                if request.method == 'DELETE':
                    shoppinglist.delete()
                    return {
                    "message" : "shoppinglist {} deleted successfully".format(shoppinglist.id)
                    },200
            else:
                message = user_id
                response = {
                "message" : message
                }
                return make_response(jsonify(response)), 401

    @app.route('/shoppinglists/<int:list_id>/items', methods=['POST', 'GET'])
    def shoppinglist_item(user_id, list_id):
        """
        Create and get all shopping list items 
        """
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]
        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance (user_id, str):
                if request.method == 'POST':
                    name = str(request.data.get('name', ''))
                    if name:
                        shoppinglistitem = ShoppingListItems(name=name, list_id=list_id)
                        shoppinglistitem.save()
                        response = jsonify({
                            'id': shoppinglistitem.id,
                            'name': shoppinglistitem.name,
                            'date_created': shoppinglistitem.date_created,
                            'date_modified': shoppinglistitem.date_modified
                        })
                        return make_response(response), 201
                else:
                    shoppinglistitems = ShoppingListItems.get_all(list_id)
                    results = []
                    for shoppinglistitem in shoppinglistitems:
                        obj = {
                        'id': shoppinglistitem.id,
                        'name': shoppinglistitem.name,
                        'date_created': shoppinglistitem.date_created,
                        'date_modified': shoppinglistitem.date_modified
                        }
                        results.append(obj)
                    response = jsonify(results)
                    return make_response(response), 200
            else:
                message = user_id
                response = {
                'message' : message
                }
                return make_response(jsonify(response)), 401

    @app.route('/shoppinglists/<int:list_id>/items/<int:item_id>', methods=['GET'])
    def get_item_by_id(user_id, list_id):
        """
        Get a shopping list item created by its id
        """
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]
        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance (user_id, str):
                shoppinglistitem = ShoppingListItems.query.filter_by(id=item_id, list_id=list_id).first()
                if shoppinglistitem.list_id == list_id:
                    response = jsonify({
                        'id': shoppinglistitem.id,
                        'name': shoppinglistitem.name,
                        'date_created': shoppinglistitem.date_created,
                        'date_modified': shoppinglistitem.date_modified
                    })
                    response.status_code = 200
                    return response
                else:
                    abort(404)
            else:
                message = user_id
                response = {
                'message': message
                }
                return make_response(jsonify(response)), 401

    @app.route('/shoppinglists/<int:list_id>/items/<int:item_id>', methods=['PUT'])
    def item_editing(user_id, list_id):
        """
        Update a shopping list item
        """
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]
        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance (user_id, str):
                shoppinglistitem = ShoppingListItems.query.filter_by(id=item_id, list_id=list_id).first()
                if not shoppinglistitem:
                    abort(404)
                if request.method == 'PUT':
                    name = str(request.data.get('name', ''))
                    shoppinglistitem.name = name
                    shoppinglistitem.save()
                    response = jsonify({
                        'id': shoppinglistitem.id,
                        'name': shoppinglistitem.name,
                        'date_created': shoppinglistitem.date_created,
                        'date_modified': shoppinglistitem.date_modified
                    })
                    response.status_code = 200
                    return response
            else:
                message = user_id
                response = {
                'message': message
                }
                return make_response(jsonify(response)), 401

    @app.route('/shoppinglists/<int:list_id>/items/<int:item_id>', methods=['DELETE'])
    def item_deletion(user_id, list_id):
        """
        Delete a shoppinglist item
        """
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]
        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance (user_id, str):
                shoppinglistitem = ShoppingListItems.query.filter_by(id=item_id, list_id=list_id).first()
                if not shoppinglistitem:
                    abort(404)
                if request.method == 'DELETE':
                    shoppinglistitem.delete()
                    return {
                    "message" : "shoppinglist item {} has been deleted successfully".format(shoppinglistitem.id)
                    },200
            else:
                message = user_id
                response = {
                'message': message
                }
                return make_response(jsonify(response)), 401

    from .auth import auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app
