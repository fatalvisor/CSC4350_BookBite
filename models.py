# Note: Be sure to install wtforms, flask_wtf, and wtforms.validators onto your system.
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, SubmitField, PasswordField, SelectField, RadioField
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Length, ValidationError, Optional

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
    """Establishes the basic fields required for a form used to update a user's username and email information."""

    username = StringField("Username", validators=[InputRequired()])
    email = StringField("Email", validators=[InputRequired()])

    submit = SubmitField("Update")


# =====================================================================
# SECTION 2: FORMS USED FOR CRITICAL FUNCTIONS IN PRIMARY HTML PAGES
# =====================================================================
class BookInfoFormAdd(FlaskForm):
    """Establishes the basic fields required for a form used to pull certain information about a displayed book given an ISBN. A favorite button is also provided."""

    original_route = StringField(render_kw={"readonly": True})

    isbn = StringField(
        validators=[Length(min=1, max=15)], render_kw={"readonly": True},
    )
    submit_explore = SubmitField(label="Explore")
    submit_add = SubmitField(label="Favorite")


class BookInfoFormSendRecs(FlaskForm):
    """Establishes the basic fields required for a form used to pull certain information about a displayed book or send a specific user a recommendation."""

    isbn = StringField(
        validators=[Length(min=1, max=15)], render_kw={"readonly": True},
    )
    receiver_username = StringField(
        validators=[Length(min=1, max=80), Optional()],
        render_kw={"placeholder": "Friend's Username"},
    )
    submit_explore = SubmitField(label="Explore")
    submit_delete = SubmitField(label="Unfavorite")
    submit_recommend = SubmitField(label="Recommend")


class BookInfoFormDeleteRecs(FlaskForm):
    """Establishes the basic fields required for a form used to pull certain information about a displayed book or delete a recommendation from other users."""

    isbn = StringField(
        validators=[Length(min=1, max=15)], render_kw={"readonly": True},
    )
    receiver_username = StringField(
        validators=[Length(min=1, max=80), Optional()],
        render_kw={"placeholder": "Friend's Username"},
    )
    submit_explore = SubmitField(label="Explore")
    submit_favorite = SubmitField(label="Favorite")
    submit_delete = SubmitField(label="Not Interested")


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
        validators=[InputRequired(), Length(min=1, max=100)],
        render_kw={"placeholder": "Title"},
    )
    submit = SubmitField("Submit")


class ReviewForm(FlaskForm):
    """Fields required for a review form"""

    isbn = StringField(
        validators=[Length(min=1, max=15)], render_kw={"readonly": True},
    )
    comment = StringField(
        validators=[Length(min=1, max=200), Optional()],
        render_kw={"placeholder": "Add a comment"},
    )
    rating = RadioField(
        "Rating", choices=[("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5")],
    )
    submit = SubmitField("Submit")


# =====================================================================
# SECTION 3: FORMS WITH SINGLE-PURPOSE BUTTONS
# =====================================================================
class ReturnHomeButton(FlaskForm):
    """Creates a form with a single button to send the user back to the homepage when clicked."""

    submit = SubmitField("Return Home")


class LogoutButton(FlaskForm):
    """Creates a form with a single button to send the user back to the login page when clicked.."""

    submit = SubmitField("Logout")


# =====================================================================
# SECTION 4: DATABASE MODELS
# =====================================================================
class Users(db.Model, UserMixin):
    """Defines a "Users" table in the database with three basic attributes outside of id: the user's username, email, and password."""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)


class Favorites(db.Model):
    """Defines a "Favorites" table in the database with two basic attributes outside of ID: the user's email and the ISBN of the favorited book."""

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    bookISBN = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return "<Favorites %r>" % self.bookISBN


class Recommendations(db.Model):
    """Defines a "Recommendations" table in the database with three basic attributes outside of ID: the sender's name, receiver's name, and ISBN of the recommended book."""

    id = db.Column(db.Integer, primary_key=True)
    senderUsername = db.Column(db.String(80), nullable=False)
    receiverUsername = db.Column(db.String(80), nullable=False)
    bookISBN = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return "<Favorites %r>" % self.bookISBN


class Review(db.Model):
    """ "Creating Review table"""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False)
    isbn = db.Column(db.String(20), nullable=False)
    comment = db.Column(db.String(200), nullable=False)
    rating = db.Column(db.String(15), nullable=False)

    def __repr__(self):
        """ "Creating Review table"""
        return f"<User {self.username}>"

    def get_username(self):
        """ "Creating Review table"""
        return self.username
