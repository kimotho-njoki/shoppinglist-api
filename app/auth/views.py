import re
from . import auth_blueprint
from flask.views import MethodView
from flask import Blueprint, make_response, request, jsonify
from flask_bcrypt import Bcrypt
from app.models import User

class RegistrationView(MethodView):
    """
    This class-based view handles registration of users
    """
    def post(self):
        """
        Handles POST requests
        """
        username = str(request.data.get('username'))
        email = str(request.data.get('email'))
        password = str(request.data.get('password'))
        regex = r"(^[a-zA-Z0-9_.]+@[a-zA-Z0-9-]+\.[a-z]+$)"
        if re.match("^[a-zA-Z0-9 _]*$", username) and username.strip():
            if re.match(regex, email) and email.strip():
                if len(password) > 6 and password.strip():
                    user = User.query.filter_by(username=username, email=email).first()

                    if not user:
                        try:
                            username = request.data['username']
                            email = request.data['email']
                            password = request.data['password']
                            user = User(username=username, email=email, password=password)
                            user.save()
                            response = {
                            'message': "Registration successful."
                            }
                            return make_response(jsonify(response)), 201
                        except Exception as e:
                            response = {
                            'message': str(e)
                            }
                            return make_response(jsonify(response)), 401
                    else:
                        response = {
                        'message': "You are already registered. Please login."
                        }
                        return make_response(jsonify(response)), 302
                else:
                    response = {
                    'message': "Password is either too short or empty."\
            "Please try again."
                    }
                    return make_response(jsonify(response)), 403
            else:
                response = {
                'message': "Email Invalid."\
            "Do not include special characters or leave the field empty."
                }
                return make_response(jsonify(response)), 403
        else:
            response = {
            'message': "Username can neither include special"\
            "characters nor be empty."
            }
            return make_response(jsonify(response)), 403

class LoginView(MethodView):
    """
    This class-based view handles login of users and generation of access tokens
    """
    def post(self):
        """
        Handles POST requests
        """
        username = str(request.data.get('username'))
        email = str(request.data.get('email'))
        password = str(request.data.get('password'))
        if username.strip():
            if email.strip():
                if password.strip():
                    try:
                        user = User.query.filter_by(username=username, email=email).first()
                        if user and user.password_is_valid(password):
                            access_token = user.encode_auth_token(user.id)
                            if access_token:
                                response = {
                                'message': 'You logged in successfully.',
                                'username': username,
                                'user_id': user.id,
                                'access_token' : access_token.decode()
                                }
                                return make_response(jsonify(response)), 200
                        else:
                            response = {
                            'message': "Login unsuccessful."\
            "Please register or confirm details."
                            }
                            return make_response(jsonify(response)), 401
                    except Exception as e:
                        response = {
                        'message': str(e)
                        }
                        return make_response(jsonify(response)), 500
                else:
                    response = {
                    'message': "Password cannot be empty."
                    }
                    return make_response(jsonify(response)), 403
            else:
                response = {
                'message': "Email cannot be empty."
                }
                return make_response(jsonify(response)), 403
        else:
            response = {
            'message': "Username cannot be empty."
            }
            return make_response(jsonify(response)), 403

    def put(self, user_id):
        """
        Handles PUT requests
        """
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]
        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                user = User.query.filter_by(id=user_id).first()
                if not user:
                    response = {
                    'message': "User does not exist."
                    }
                    return make_response(jsonify(response)), 404
                else:
                    username = str(request.data.get('username', user.username))
                    email = str(request.data.get('email', user.email))
                    password = str(request.data.get('password', user.password))
                    regex = r"(^[a-zA-Z0-9_.]+@[a-zA-Z0-9-]+\.[a-z]+$)"
                
                    if re.match("^[a-zA-Z0-9 _]*$", username) and username.strip():
                        if re.match(regex, email) and email.strip():
                            if len(password) > 6 and password.strip():
                                user.username = username
                                user.email = email
                                user.password = password
                                user.save()
                                response = {
                                'current_username': user.username,
                                'current_email': user.email,
                                'current_password': user.password
                                }
                                return make_response(jsonify(response)), 200
                            else:
                                response = {
                                'message': "Password is either too short or empty."
                                }
                                return make_response(jsonify(response)), 400
                        else:
                            response = {
                            'message': "Email Invalid. Please input field with correct format."
                            }
                            return make_response(jsonify(response)), 400
                    else:
                        response = {
                        'message': "Username can neither include special characters nor be empty."
                        }
                        return make_response(jsonify(response)), 400
            else:
                message = user_id
                response = {
                'message': message
                }
                return make_response(jsonify(response)), 401

class PasswordResetView(MethodView):
    """
    This class-based view handles the reseting of a users password
    """
    def put(self):
        """
        Handles POST request
        """
        email = str(request.data.get('email'))
        password = str(request.data.get('password'))
        regex = r"(^[a-zA-Z0-9_.]+@[a-zA-Z0-9-]+\.[a-z]+$)"
        if re.match(regex, email) and email.strip():
            if len(password) > 6 and password.strip():
                user = User.query.filter_by(email=email).first()
                if user:
                    user.password = Bcrypt().generate_password_hash(password).decode()
                    user.save()
                    response = {
                    'message': "Password reset. You can now login with new password."
                    }
                    return make_response(jsonify(response)), 200
                else:
                    response = {
                    'message': "User email does not exist."
                    }
                    return make_response(jsonify(response)), 404
            else:
                response = {
                'message': "Password is either too short or empty."
                }
                return make_response(jsonify(response)), 400
        else:
            response = {
            'message': "Email Invalid. Do not include special characters nor leave field empty."
            }
            return make_response(jsonify(response)), 400

# define the API resource
registration_view = RegistrationView.as_view('registration_view')
login_view = LoginView.as_view('login_view')
reset_view = PasswordResetView.as_view('reset_view')

# define the API Endpoints
auth_blueprint.add_url_rule(
    '/auth/register',
    view_func=registration_view,
    methods=['POST'])

auth_blueprint.add_url_rule(
    '/auth/login',
    view_func=login_view,
    methods=['POST'])

auth_blueprint.add_url_rule(
    '/auth/login/<int:user_id>',
    view_func=login_view,
    methods=['PUT'])

auth_blueprint.add_url_rule(
    '/auth/reset',
    view_func=reset_view,
    methods=['PUT'])
   