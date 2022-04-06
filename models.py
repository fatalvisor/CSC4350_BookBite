from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


class Users(UserMixin, db.Model):
    """Defines a "Users" table in the database with two basic attributes, an ID and the user's login email."""

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return "<User %r>" % self.email


class Favorites(db.Model):
    """Defines a "Favorites" table in the database with three basic attributes: an ID, the user's email, and the ISBN of the favorited book."""

    id = db.Column(db.Integer, primary_key=True)
    userEmail = db.Column(db.String(100), nullable=False)
    bookISBN = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "<Review %r>" % self.bookISBN
