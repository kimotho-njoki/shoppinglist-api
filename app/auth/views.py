from . import auth_blueprint
from flask.views import MethodView
from flask import make_response, request, jsonify
from app.models import User

class RegistrationView(MethodView):
	"""
	This class-based view handles registration of users
	"""
	def post(self):
		"""
		Handles POST requests
		"""
		user = User.query.filter_by(username=request.data['username']).first()

		if not user:
			try:
				post_data = request.data
				username = post_data['username']
				email = post_data['email']
				password = post_data['password']
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
			return make_response(jsonify(response)), 202

class LoginView(MethodView):
	"""
	This class-based view handles login of users and generation of access tokens
	"""
	def post(self):
		"""
		Handles POST requests
		"""
		try:
			user = User.query.filter_by(username=request.data['username']).first()

			if user and user.password_is_valid(request.data['password']):
				access_token = user.encode_auth_token(user.id)
				if access_token:
					response = {
					'message': 'You logged in successfully.',
					'access_token' : access_token.decode()
					}
					return make_response(jsonify(response)), 200
			else:
				response = {
				'message': 'Login unsuccessful. Please register or confirm details.'
				}
				return make_response(jsonify(response)), 401
		except Exception as e:
			response = {
			'message': str(e)
			}
			return make_response(jsonify(response)), 500

# define the API resource
registration_view = RegistrationView.as_view('registration_view')
login_view = LoginView.as_view('login_view')

# define the API Endpoints
auth_blueprint.add_url_rule(
	'/auth/register',
	view_func=registration_view,
	methods=['POST'])

auth_blueprint.add_url_rule(
	'/auth/login',
	view_func=login_view,
	methods=['POST'])
