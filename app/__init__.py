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
                    if name and not name == '':
                        if ShoppingList.query.filter_by(
                            name=name, user_id=user_id).first() is not None:
                            response = {
                            'message': "Shoppinglist name already exists."
                            }
                            return make_response(jsonify(response)), 302

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
                        response = {
                        'message': "Please enter a name."
                        }
                        return make_response(jsonify(response)), 400
                else:
                    search_query = request.args.get("q")
                    try:
                        limit = int(request.args.get('limit', 10))
                        page_no = int(request.args.get('page', 1))
                    except ValueError:
                        response = {
                        'message': "Input must be an integer"
                        }
                        return make_response(jsonify(response)), 400

                    if search_query:
                        shoppinglists = ShoppingList.query.filter(ShoppingList.name.ilike(
                            '%' + search_query + '%')).filter_by(user_id=user_id).all()
                        results = []
                        if not shoppinglists:
                            response = {
                            'message': "No shoppinglist found matching your input"
                            }
                            return make_response(jsonify(response)), 404
                        for shoppinglist in shoppinglists:
                            obj = {
                            'id': shoppinglist.id,
                            'name': shoppinglist.name,
                            'date_created': shoppinglist.date_created,
                            'date_modified': shoppinglist.date_modified
                            }
                            results.append(obj)
                        response = jsonify(results)
                        return make_response(response), 200

                    paginated_shoplists = ShoppingList.query.filter_by(
                        user_id=user_id).paginate(page_no, limit)
                    all_results = []

                    if not paginated_shoplists:
                        response = {
                        'message': "You do not have any shoppinglists"
                        }
                        return make_response(jsonify(response)), 404
                    for shoplist in paginated_shoplists.items:
                        obj = {
                        'id': shoplist.id,
                        'name': shoplist.name,
                        'date_created': shoplist.date_created,
                        'date_modified' : shoplist.date_modified
                        }
                        all_results.append(obj)
                    return make_response(jsonify(all_results)), 200
            else:
                message = user_id
                response = {
                'message' : message
                }
                return make_response(jsonify(response)), 401

    @app.route('/shoppinglists/<int:list_id>', methods=['GET'])
    def get_shoppinglist(list_id):
        """
        Get shoppinglist by id
        """
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]
        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance (user_id, str):
                shoppinglist = ShoppingList.query.filter_by(id=list_id, user_id=user_id).first()
                if shoppinglist:
                    response = jsonify({
                        'id' : shoppinglist.id,
                        'name' : shoppinglist.name,
                        'date_created' : shoppinglist.date_created,
                        'date_modified' : shoppinglist.date_modified
                    })
                    response.status_code = 200
                    return response
                else:
                    response = {
                    'message': "Shoppinglist does not exist"
                    }
                    return make_response(jsonify(response)), 404
            else:
                message = user_id
                response = {
                'message' : message
                }
                return make_response(jsonify(response)), 401

    @app.route('/shoppinglists/<int:list_id>', methods=['PUT'])
    def edit_shoppinglist(list_id):
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
                    response = {
                    'message': "Shoppinglist does not exist"
                    }
                    return make_response(jsonify(response)), 404
                if request.method == 'PUT':
                    name = str(request.data.get('name', ''))
                    if name and not name == '':
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
                        response = {
                        'message': "Please enter a name."
                        }
                        return make_response(jsonify(response)), 400
            else:
                message = user_id
                response = {
                "message" : message
                }
                return make_response(jsonify(response)), 401

    @app.route('/shoppinglists/<int:list_id>', methods=['DELETE'])
    def delete_shoppinglist(list_id):
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
                    response = {
                    'message': "Shoppinglist does not exist"
                    }
                    return make_response(jsonify(response)), 404
                if request.method == 'DELETE':
                    shoppinglist.delete()
                    return {
                    "message" : "shoppinglist {} deleted successfully".format(shoppinglist.name)
                    },200
            else:
                message = user_id
                response = {
                "message" : message
                }
                return make_response(jsonify(response)), 401

    @app.route('/shoppinglists/<int:list_id>/items', methods=['POST', 'GET'])
    def shoppinglist_item(list_id):
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
                    budgeted_amount = request.data.get('budgeted_amount', 0)
                    if name and not name == '':
                        if ShoppingListItems.query.filter_by(
                            name=name, list_id=list_id).first() is not None:
                            response = {
                            'message': "Item name already exists."
                            }
                            return make_response(jsonify(response)), 302
                        if not isinstance (budgeted_amount, str) and not budgeted_amount == '':
                            shoppinglistitem = ShoppingListItems(name=name, budgeted_amount=budgeted_amount, list_id=list_id)
                            shoppinglistitem.save()
                            response = jsonify({
                                'id': shoppinglistitem.id,
                                'name': shoppinglistitem.name,
                                'budgeted_amount': shoppinglistitem.budgeted_amount,
                                'date_created': shoppinglistitem.date_created,
                                'date_modified': shoppinglistitem.date_modified
                            })
                            return response, 201
                        else:
                            response = {
                            'message': "Input must be a number. It cannot be empty."
                            }
                            return make_response(jsonify(response)), 400
                    else:
                        response = {
                        'message': "Please enter a name."
                        }
                        return make_response(jsonify(response)), 400
                else:
                    search_query = request.args.get("q")
                    try:
                        limit = int(request.args.get('limit', 10))
                        page_no = int(request.args.get('page', 1))
                    except ValueError:
                        response = {
                        'message': "Input must be an integer"
                        }
                        return make_response(jsonify(response)), 400

                    if search_query:
                        shoppinglistitems = ShoppingListItems.query.filter(
                            ShoppingListItems.name.ilike('%' + search_query + '%')).filter_by(
                            list_id=list_id).all()
                        results = []

                        if not shoppinglistitems:
                            response = {
                            'message': "No shopping items matching your input"
                            }
                            return make_response(jsonify(response)), 404
                        for shoppinglistitem in shoppinglistitems:
                            obj = {
                            'id': shoppinglistitem.id,
                            'name': shoppinglistitem.name,
                            'budgeted_amount': shoppinglistitem.budgeted_amount,
                            'date_created': shoppinglistitem.date_created,
                            'date_modified': shoppinglistitem.date_modified
                            }
                            results.append(obj)
                        response = jsonify(results)
                        return response, 200

                    paginated_shopitems = ShoppingListItems.query.filter_by(
                        list_id=list_id).paginate(page_no, limit)
                    all_results = []

                    if not paginated_shopitems:
                        response = {
                        'message' : "Your shoppinglist has no items"
                        }
                        return make_response(jsonify(response)), 404
                    for shopitem in paginated_shopitems.items:
                        obj = {
                        'id': shopitem.id,
                        'name': shopitem.name,
                        'budgeted_amount': shopitem.budgeted_amount,
                        'date_created': shopitem.date_created,
                        'date_modified': shopitem.date_modified
                        }
                        all_results.append(obj)
                    response = jsonify(all_results)
                    return response
            else:
                message = user_id
                response = {
                'message' : message
                }
                return make_response(jsonify(response)), 401

    @app.route('/shoppinglists/<int:list_id>/items/<int:item_id>', methods=['GET'])
    def get_item_by_id(list_id, item_id):
        """
        Get a shopping list item created by its id
        """
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]
        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance (user_id, str):
                shoppinglistitem = ShoppingListItems.query.filter_by(id=item_id, list_id=list_id).first()
                if shoppinglistitem:
                    response = jsonify({
                        'id': shoppinglistitem.id,
                        'name': shoppinglistitem.name,
                        'budgeted_amount': shoppinglistitem.budgeted_amount,
                        'date_created': shoppinglistitem.date_created,
                        'date_modified': shoppinglistitem.date_modified
                    })
                    response.status_code = 200
                    return response
                else:
                    response = {
                    'message': "Item does not exist"
                    }
                    return make_response(jsonify(response)), 404
            else:
                message = user_id
                response = {
                'message': message
                }
                return make_response(jsonify(response)), 401

    @app.route('/shoppinglists/<int:list_id>/items/<int:item_id>', methods=['PUT'])
    def item_editing(list_id, item_id):
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
                    response = {
                    'message': "Item does not exist"
                    }
                    return make_response(jsonify(response)), 404
                if request.method == 'PUT':
                    name = str(request.data.get('name', ''))
                    budgeted_amount = request.data.get('budgeted_amount', 0)
                    if name and not name == '':
                        if not isinstance (budgeted_amount, str) and not budgeted_amount == '':
                            shoppinglistitem.name = name
                            shoppinglistitem.budgeted_amount = budgeted_amount
                            shoppinglistitem.save()
                            response = jsonify({
                                'id': shoppinglistitem.id,
                                'name': shoppinglistitem.name,
                                'budgeted_amount': shoppinglistitem.budgeted_amount,
                                'date_created': shoppinglistitem.date_created,
                                'date_modified': shoppinglistitem.date_modified
                            })
                            response.status_code = 200
                            return response
                        else:
                            response = {
                            'message': "Input must be a number. It cannot be empty."
                            }
                            return make_response(jsonify(response)), 400
                    else:
                        response = {
                        'message': "Please enter a name."
                        }
                        return make_response(jsonify(response)), 400
            else:
                message = user_id
                response = {
                'message': message
                }
                return make_response(jsonify(response)), 401

    @app.route('/shoppinglists/<int:list_id>/items/<int:item_id>', methods=['DELETE'])
    def item_deletion(list_id, item_id):
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
                    response = {
                    'message': "Item does not exist"
                    }
                    return make_response(jsonify(response)), 404
                if request.method == 'DELETE':
                    shoppinglistitem.delete()
                    return {
                    "message" : "shoppinglist item {} has been deleted successfully".format(shoppinglistitem.name)
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
