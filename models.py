# Be sure to install wtforms, flask_wtf, and wtforms.validators onto your system.
from app import app
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, SubmitField, PasswordField
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Length, ValidationError

db = SQLAlchemy()


class SignupForm(FlaskForm):
    email = StringField(
        validators=[InputRequired(), Length(min=1, max=64)],
        render_kw={"placeholder": "Email"},
    )

    username = StringField(
        validators=[InputRequired(), Length(min=1, max=15)],
        render_kw={"placeholder": "Username"},
    )

    password = PasswordField(
        validators=[InputRequired(), Length(min=2, max=10)],
        render_kw={"placeholder": "Password"},
    )

    submit = SubmitField("Sign Up")

    def validate_email(self, email):
        existing_email = Users.query.filter_by(email=email.data).first()

        if existing_email:
            raise ValidationError("That email already exists.")

    def validate_username(self, username):
        existing_username = Users.query.filter_by(username=username.data).first()

        if existing_username:
            raise ValidationError("That Username already exists.")


class LoginForm(FlaskForm):
    email = StringField(
        validators=[InputRequired(), Length(min=2, max=10)],
        render_kw={"placeholder": "Email"},
    )

    submit = SubmitField("Login")

    password = PasswordField(
        validators=[InputRequired(), Length(min=2, max=10)],
        render_kw={"placeholder": "Password"},
    )


class Users(db.Model, UserMixin):
    """Defines a "Users" table in the database with two basic attributes, an ID and the user's login email."""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)


class Favorites(db.Model):
    """Defines a "Favorites" table in the database with three basic attributes: an ID, the user's email, and the ISBN of the favorited book."""

    id = db.Column(db.Integer, primary_key=True)
    userEmail = db.Column(db.String(100), nullable=False)
    bookISBN = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "<Review %r>" % self.bookISBN
