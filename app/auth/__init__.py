from flask import Blueprint

#create the blueprint object
auth_blueprint = Blueprint('auth', __name__)

from . import views
