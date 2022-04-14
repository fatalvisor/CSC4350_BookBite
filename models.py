# Note: Be sure to install wtforms, flask_wtf, and wtforms.validators onto your system.
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, SubmitField, PasswordField, SelectField
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Length, ValidationError

db = SQLAlchemy()


class SignupForm(FlaskForm):
    """Establishes the basic fields required for a sign-up form instance."""

    email = StringField(
        validators=[InputRequired(), Length(min=1, max=64)],
        render_kw={"placeholder": "Email"},
    )

    username = StringField(
        validators=[InputRequired(), Length(min=1, max=15)],
        render_kw={"placeholder": "Username"},
    )

    password = PasswordField(
        validators=[InputRequired(), Length(min=2, max=15)],
        render_kw={"placeholder": "Password"},
    )

    submit = SubmitField("Sign Up")

    def validate_email(self, email):
        """Checks if a user with a specific email already exists in the database. If so, throw a warning."""
        existing_email = Users.query.filter_by(email=email.data).first()

        if existing_email:
            raise ValidationError("That email already exists.")

    def validate_username(self, username):
        """Checks if a user with a specific username already exists in the database. If so, throw a warning."""
        existing_username = Users.query.filter_by(username=username.data).first()

        if existing_username:
            raise ValidationError("That Username already exists.")


class LoginForm(FlaskForm):
    """Establishes the basic fields required for a login form instance."""

    email = StringField(
        validators=[InputRequired(), Length(min=2, max=64)],
        render_kw={"placeholder": "Email"},
    )

    submit = SubmitField("Login")

    password = PasswordField(
        validators=[InputRequired(), Length(min=2, max=10)],
        render_kw={"placeholder": "Password"},
    )


class SuggestionInfoForm(FlaskForm):
    """Establishes the basic fields required for a form used to pull certain information for suggested or displayed books given an ISBN."""

    isbn = StringField(
        validators=[InputRequired(), Length(min=1, max=15)],
        render_kw={"readonly": True},
    )
    submit = SubmitField("Explore")


class BookThemeForm(FlaskForm):
    """Establishes the basic fields required for a form used to select a theme out of a list of options."""

    # Note: Theme options must be added here For simplicity sake, dummyValue = dummyName.
    theme = SelectField(
        "theme",
        choices=[
            ("Adventure", "Adventure"),
            ("Humor", "Humor"),
            ("Horror", "Horror"),
            ("Fantasy", "Fantasy"),
            ("Supernatural", "Supernatural"),
            ("Media", "Media"),
            ("Good vs. Evil", "Good vs. Evil"),
            ("Determination", "Determination"),
            ("Friendship", "Friendship"),
            ("Science Fiction", "Science Fiction"),
            ("Animals", "Animals"),
            ("Halloween", "Halloween"),
            ("Classics", "Classics"),
            ("Survival", "Survival"),
            ("Coming of Age", "Coming of Age"),
            ("War", "War"),
            ("Love & Romance", "Love & Romance"),
            ("Patriotism", "Patriotism"),
            ("Betrayal", "Betrayal"),
            ("Geography", "Geography"),
            ("Self-Discovery", "Self-Discovery"),
            ("Science & Nature", "Science & Nature"),
            ("Fairytales & Fables", "Fairytales & Fables"),
            ("Family & Relationships", "Family & Relationships"),
        ],
    )
    submit = SubmitField("Submit")


class BookTitleForm(FlaskForm):
    """Establishes the basic fields required for a form used to pull certain book information given a title."""

    title = StringField(
        validators=[InputRequired(), Length(min=1, max=20)],
        render_kw={"placeholder": "Title"},
    )
    submit = SubmitField("Submit")


class FavoritesForm(FlaskForm):
    """Establishes the basic fields required for a form used to add or delete a favorite book by ISBN."""

    isbn = StringField(
        validators=[InputRequired(), Length(min=1, max=15)],
        render_kw={"placeholder": "isbn"},
    )
    submit = SubmitField("Submit")


class ReturnHomeButton(FlaskForm):
    """Creates a form with a single button to send the user back to the homepage when clicked.."""

    submit = SubmitField("Return home")


class LogoutButton(FlaskForm):
    """Creates a form with a single button to send the user back to the login page when clicked.."""

    submit = SubmitField("Logout")


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
    bookISBN = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return "<Favorites %r>" % self.bookISBN
