from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify, abort, make_response

from instance.config import app_config

db = SQLAlchemy()

def create_app(config_name):
    from app.models import ShoppingList, User
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICAIONS']=False
    #prepare application to work with SQLAlchemy
    db.init_app(app)

    @app.route('/shoppinglists/', methods=['POST', 'GET'])
    def shoppinglists():
        #create and retrieve all shoppinglists
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]

        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance (user_id, str):
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
                        return make_response(response), 201
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
                        return make_response(response), 200
            else:
                message = user_id
                response = {
                'message' : message
                }
                return make_response(jsonify(response)), 401


        @app.route('/shoppinglists/<int:list_id>', methods=['GET'])
        def get_shoppinglist(user_id, list_id):
            auth_header = request.headers.get('Authorization')
            access_token = auth_header.split(" ")[1]

            if access_token:
                user_id = User.decode_token(access_token)
                if not isinstance (user_id, str):
                    shoppinglist = ShoppingList.query.filter_by(id=list_id, user_id=user_id).first()
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

        @app.route('/shoppinglist/<int:list_id>', methods=['DELETE'])
        def delete_shoppinglist(user_id, list_id):
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

    from .auth import auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app
