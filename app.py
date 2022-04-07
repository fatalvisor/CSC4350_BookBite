# Be sure to install bcrypt and flask-bcrypt onto your system.
import os
import flask
import bcrypt
from flask_bcrypt import Bcrypt
from flask_login import (
    LoginManager,
    login_user,
    login_required,
    logout_user,
    current_user,
)
from dotenv import find_dotenv, load_dotenv
from penguin import book_search
from models import db, SignupForm, LoginForm, Users, Favorites

app = flask.Flask(__name__)
load_dotenv(find_dotenv())
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL_V2")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = os.getenv("secret_key")
bcrypt = Bcrypt(app)

bp = flask.Blueprint(
    "bp",
    __name__,
    template_folder="./static/react",
)

db.init_app(app)
with app.app_context():
    db.create_all()
    login_manager = LoginManager()
    login_manager.login_view = "login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        """Returns the user associated with a specific user ID."""
        return Users.query.get(int(user_id))


@app.route("/", methods=["GET", "POST"])
def signup():
    """Registers a new user to the database, assuming there is no user with the same username."""
    form = SignupForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        new_user = Users(email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return flask.redirect(flask.url_for("login"))

    return flask.render_template("signup.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Checks login credentials; if valid, redirect the user to the homepage. Otherwise, re-render the login page."""
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return flask.redirect(flask.url_for("homepage"))

    return flask.render_template("login.html", form=form)


@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    """Clears the current user's session cookies and redirects you back to the login page."""
    logout_user()
    return flask.redirect(flask.url_for("login"))


@app.route("/handle_theme_suggestions")
def handle_theme_suggestions():
    """Based on the theme selected, the title and cover image of a random book under said theme is returned and rendered in a webpage."""
    data = flask.request.form
    book_titles, book_urls, book_ISBNs = book_search(data["theme"])
    num_books = len(book_titles)
    return flask.render_template(
        # At the time of writing this (4/05), no homepage.html webpage currently exists. This is just a placeholder for now.
        "test.html",
        book_titles=book_titles,
        book_urls=book_urls,
        book_ISBNs=book_ISBNs,
        num_books=num_books,
    )


# Route for serving React page
@bp.route("/getbook")
def getbook():
    return flask.render_template("index.html")


app.register_blueprint(bp)
app.run(host=os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT", 8080)), debug=True)
