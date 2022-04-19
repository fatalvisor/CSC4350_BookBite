# Note: Be sure to install wtforms, flask_wtf, and wtforms.validators onto your system.
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, SubmitField, PasswordField, SelectField
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Length, ValidationError

db = SQLAlchemy()

# =====================================================================
# SECTION 1: SIGN-UP/LOGIN FORMS
# =====================================================================
class SignupForm(FlaskForm):
    """Establishes the basic fields required for a sign-up form instance."""

    email = StringField(
        validators=[InputRequired(), Length(min=1, max=64)],
        render_kw={"placeholder": "Email"},
    )

    username = StringField(
        validators=[InputRequired(), Length(min=1, max=40)],
        render_kw={"placeholder": "Username"},
    )

    password = PasswordField(
        validators=[InputRequired(), Length(min=2, max=40)],
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
        validators=[InputRequired(), Length(min=2, max=40)],
        render_kw={"placeholder": "Password"},
    )


class UserForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    email = StringField("Email", validators=[InputRequired()])

    submit = SubmitField("Update")


# =====================================================================
# SECTION 2: FORMS USED FOR CRITICAL FUNCTIONS IN PRIMARY HTML PAGES
# =====================================================================
class BookInfoFormAdd(FlaskForm):
    """Establishes the basic fields required for a form used to pull certain information about a displayed book or add a new favorite book, given an ISBN."""

    original_route = StringField(render_kw={"readonly": True})

    isbn = StringField(
        validators=[Length(min=1, max=15)],
        render_kw={"readonly": True},
    )
    submit_explore = SubmitField(label="Explore")
    submit_add_favorite = SubmitField(label="Favorite")


class BookInfoFormDelete(FlaskForm):
    """Establishes the basic fields required for a form used to pull certain information about a displayed book or delete a favorite book, given an ISBN."""

    original_route = StringField(render_kw={"readonly": True})
    isbn = StringField(
        validators=[Length(min=1, max=15)],
        render_kw={"readonly": True},
    )
    submit_explore = SubmitField(label="Explore")
    submit_delete_favorite = SubmitField(label="Unfavorite")


class BookThemeForm(FlaskForm):
    """Establishes the basic fields required for a form used to select a theme out of a list of options."""

    # Note: Theme options must be added here For simplicity sake, dummyValue = dummyName.
    theme = SelectField(
        "theme",
        choices=[
            ("Adventure", "Adventure"),
            ("Animals", "Animals"),
            ("Betrayal", "Betrayal"),
            ("Classics", "Classics"),
            ("Coming of Age", "Coming of Age"),
            ("Determination", "Determination"),
            ("Fairy Tales & Fables", "Fairy Tales & Fables"),
            ("Family & Relationships", "Family & Relationships"),
            ("Fantasy", "Fantasy"),
            ("Friendship", "Friendship"),
            ("Geography", "Geography"),
            ("Good vs. Evil", "Good vs. Evil"),
            ("Halloween", "Halloween"),
            ("Horror", "Horror"),
            ("Humor", "Humor"),
            ("Love & Romance", "Love & Romance"),
            ("Media", "Media"),
            ("Patriotism", "Patriotism"),
            ("Science & Nature", "Science & Nature"),
            ("Science Fiction", "Science Fiction"),
            ("Self-Discovery", "Self-Discovery"),
            ("Supernatural", "Supernatural"),
            ("Survival", "Survival"),
            ("War", "War"),
        ],
    )
    submit = SubmitField("Submit")


class BookTitleForm(FlaskForm):
    """Establishes the basic fields required for a form used to pull certain information about a book, given a title."""

    title = StringField(
        validators=[InputRequired(), Length(min=1, max=40)],
        render_kw={"placeholder": "Title"},
    )
    submit = SubmitField("Submit")


# =====================================================================
# SECTION 3: FORMS WITH SINGLE-PURPOSE BUTTONS
# =====================================================================
class ReturnHomeButton(FlaskForm):
    """Creates a form with a single button to send the user back to the homepage when clicked."""

    submit = SubmitField("Return home")


class LogoutButton(FlaskForm):
    """Creates a form with a single button to send the user back to the login page when clicked.."""

    submit = SubmitField("Logout")


# =====================================================================
# SECTION 4: DATABASE MODELS
# =====================================================================
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


class Recommendations(db.Model):
    """Defines a "Recommendations" table in the database with three basic attributes: an ID, the user's email, and the ISBN of the favorited book."""

    id = db.Column(db.Integer, primary_key=True)
    userEmail = db.Column(db.String(100), nullable=False)
    senderEmail = db.Column(db.String(100), nullable=False)
    bookISBN = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return "<Favorites %r>" % self.bookISBN
