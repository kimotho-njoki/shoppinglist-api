from datetime import datetime, timedelta
from app import db
from flask_bcrypt import Bcrypt
import jwt

SECRET_KEY = 'my_secret_random_key'

class User(db.Model):
    """
    This class represents the users table
    """

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(256), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    shoplists = db.relationship('ShoppingList', order_by='ShoppingList.id', cascade="all, delete-orphan")

    def __init__(self, username, email, password):
        """
        Initialize user with a username, email and password
        """
        self.username = username
        self.email = email
        self.password = Bcrypt().generate_password_hash(password).decode()

    def password_is_valid(self, password):
        """
        Check password against its hash to validate user
        """
        return Bcrypt().check_password_hash(self.password, password)

    def save(self):
        """
        Save user details.
        This includes saving a new user and editing one
        """
        db.session.add(self)
        db.session.commit()

    def encode_auth_token(self, user_id):
        """
        Generates the authorization token
        """
        try:
            payload = {
            'exp': datetime.utcnow() + datetime.timedelta(minutes=30),
            'iat': datetime.utcnow(),
            'sub': user_id
            }

            jwt_string = jwt.encode(
                payload,
                SECRET_KEY,
                algorithm='HS256'
            )
            return jwt_string
        except Exception as e:
            return str(e)

    @staticmethod
    def decode_token(auth_token):
        """
        Decode the authorization token
        """
        try:
            payload = jwt.decode(auth_token, SECRET_KEY)
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expire. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'
            
class ShoppingList(db.Model):
    """
    This class represents the shopping lists table
    """

    __tablename__ = 'shoplists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    shoplist_items = db.relationship('ShoppingListItems', order_by='ShoppingListItems.id', cascade="all, delete-orphan")

    def __init__(self, name, user_id):
        """
        Initialize shopping list with name and user_id
        """
        self.name = name
        self.user_id = user_id

    def save(self):
        """
        Save shopping list details when creating and editing a shopping list
        """
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all(user_id):
        """
        Get all the shopping lists for the specified user
        """
        return ShoppingList.query.filter_by(user_id=user_id)

    def delete(self):
        """
        Deletes a shopping list
        """
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        """
        Return a representation of the shopping lists
        """
        return "<ShoppingList: {}>".format(self.name)

class ShoppingListItems(db.Model):
    """
    This class represents the shopping list items table
    """

    __tablename__ = 'shoplist_items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    list_id = db.Column(db.Integer, db.ForeignKey(ShoppingList.id))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __init__(self, name, list_id):
        """
        Initialize items with name and list_id
        """
        self.name = name
        self.list_id = list_id

    def save(self):
        """
        Save item details when creating and editing an item
        """
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all(list_id):
        """
        Get all items for specified shopping list
        """
        return ShoppingListItems.query.filter_by(list_id=list_id)

    def delete(self):
        """
        Deletes an item
        """
        self.session.delete(self)
        self.session.commit()

    def __repr__(self):
        """
        Returns a representation of the shopping list items
        """
        return "<ShoppingListItems: {}>".format(self.name)







