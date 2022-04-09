# Note: Be sure to install bcrypt, flask-bcrypt, and flask_wtf (if you haven't already) onto your system.
import os
import flask
import bcrypt
from dotenv import find_dotenv, load_dotenv
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect
from flask_login import (
    LoginManager,
    login_user,
    login_required,
    logout_user,
    current_user,
)
from models import (
    ReturnHomeButton,
    LogoutButton,
    db,
    SignupForm,
    LoginForm,
    SuggestionInfoForm,
    BookThemeForm,
    BookTitleForm,
    Users,
    Favorites,
)
from penguin import book_suggestions, title_search, all_book_info, basic_book_info

app = flask.Flask(__name__)
load_dotenv(find_dotenv())

app.config["SECRET_KEY"] = os.urandom(32)
app.config["WTF_CSRF_ENABLED"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL_V2")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
bcrypt = Bcrypt(app)

# CSRF protection is required to use flask_wtf's functionalities. The randomly generated secret key above is used here.
csrf = CSRFProtect()
csrf.init_app(app)

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


@app.route("/", methods=["GET"])
def signup():
    """Returns the basic sign-up page where login information can be inputted to the database."""
    form = SignupForm()
    return flask.render_template("signup.html", form=form)


@app.route("/signup_post", methods=["POST"])
def signup_post():
    """Registers a new user to the database, assuming there is no user with the same username."""
    form = SignupForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        new_user = Users(
            username=form.username.data, email=form.email.data, password=hashed_password
        )
        db.session.add(new_user)
        db.session.commit()

        return flask.redirect(flask.url_for("login"))

    return flask.redirect(flask.url_for("signup"))


@app.route("/login", methods=["GET"])
def login():
    """Returns the basic login page where login information is checked."""
    form = LoginForm()
    return flask.render_template("login.html", form=form)


@app.route("/login_post", methods=["POST"])
def login_post():
    """Checks login credentials; if valid, redirect the user to the homepage. Otherwise, re-render the login page."""
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return flask.redirect(flask.url_for("homepage"))

    return flask.redirect(flask.url_for("login"))


@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    """Clears the current user's session cookies and redirects you back to the login page."""
    logout_user()
    return flask.redirect(flask.url_for("login"))


@app.route("/homepage", methods=["GET", "POST"])
@login_required
def homepage():
    """Renders the basic landing page from which most other HTML pages can be reached."""
    logout_button = LogoutButton()
    return flask.render_template("homepage.html", logout_button=logout_button)


@app.route("/suggestions", methods=["GET", "POST"])
@login_required
def suggestions():
    """Returns the basic suggestions page where books can be suggested to the user based on a chosen theme."""
    theme_form = BookThemeForm()
    suggestion_form = SuggestionInfoForm()
    return_home_button = ReturnHomeButton()
    return flask.render_template(
        "suggestions.html",
        theme_form=theme_form,
        suggestion_form=suggestion_form,
        return_home_button=return_home_button,
    )


@app.route("/handle_theme_suggestions", methods=["GET", "POST"])
@login_required
def handle_theme_suggestions():
    """Based on the theme selected, the titles, ISBNs, and cover images of a random set of books under said theme is returned and re-rendered on the suggestions page."""
    theme_form = BookThemeForm()
    suggestion_form = SuggestionInfoForm()
    favorites_form = handle_theme_suggestions()
    if theme_form.validate_on_submit():
        book_titles, book_urls, book_ISBNs = book_suggestions(theme_form.theme.data)
        num_books = len(book_titles)
        return flask.render_template(
            "suggestions.html",
            theme_form=theme_form,
            suggestion_form=suggestion_form,
            book_titles=book_titles,
            book_urls=book_urls,
            book_ISBNs=book_ISBNs,
            num_books=num_books,
        )


@app.route("/search_by_title")
@login_required
def search_by_title():
    """Returns the basic search_by_title page where books can be searched directly for using a title input."""
    title_form = BookTitleForm()
    return flask.render_template("search_by_title.html", title_form=title_form)


@app.route("/handle_title_selection", methods=["GET", "POST"])
@login_required
def handle_title_selection():
    """Returns the basic search_by_title page."""
    title_form = BookTitleForm()
    suggestion_form = SuggestionInfoForm()
    if title_form.validate_on_submit():
        try:
            book_ISBN = title_search(title_form.title.data)
            book_title, book_url = basic_book_info(book_ISBN)
            return flask.render_template(
                "search_by_title.html",
                title_form=title_form,
                suggestion_form=suggestion_form,
                book_title=book_title,
                book_url=book_url,
                book_ISBN=book_ISBN,
                num_books=1,
            )
        except:
            return flask.render_template(
                "search_by_title.html",
                title_form=title_form,
                suggestion_form=suggestion_form,
                error=1,
            )


@app.route("/favorites")
@login_required
def favorites():
    """Displays the current user's favorited books on the "favorites" page."""
    suggestion_form = SuggestionInfoForm()
    all_favorite_isbns = Favorites.query.filter_by(userEmail=current_user.email).all()
    book_titles, book_urls = basic_book_info(all_favorite_isbns)
    num_books = len(all_favorite_isbns)
    if num_books == 0:
        return_home_button = ReturnHomeButton()
        return flask.render_template(
            "no_favorites.html", return_home_button=return_home_button
        )
    else:
        return flask.render_template(
            "favorites.html",
            suggestion_form=suggestion_form,
            book_titles=book_titles,
            book_urls=book_urls,
            book_ISBNs=all_favorite_isbns,
            num_books=num_books,
        )


# Need current user to store current user, so need to talk to maryam about user login
# And make sure that what i am doing will work.
@app.route("/add_favorite", methods=["GET", "POST"])
def add_favorite():
    isbn = flask.request.form.get("isbn")
    new_favorite = Favorites(userEmail=current_user.email, bookISBN=isbn)
    db.session.add(new_favorite)
    db.session.commit()


@app.route("/delete_favorite", methods=["GET", "POST"])
def delete_favorite():
    isbn = flask.request.form.get("isbn")
    delete_book = Favorites.query.filter_by(isbn=isbn, userEmail=current_user.email)
    db.session.delete(delete_book)
    db.session.commit()
    return flask.redirect(flask.url_for("favorites"))


@app.route("/get_book_info", methods=["POST"])
@login_required
def get_book_info():
    """Displays more specific info about a book in a separate "bookpage" page based on the provided ISBN."""
    data = flask.request.form
    book_isbn = data["isbn"]
    (
        author,
        flapcopy,
        author_bio,
        book_isbn,
        page_num,
        book_theme,
        book_cover,
        book_title,
    ) = all_book_info(book_isbn)

    return flask.render_template(
        "bookpage.html",
        author=author,
        flapcopy=flapcopy,
        author_bio=author_bio,
        book_isbn=book_isbn,
        page_num=page_num,
        book_theme=book_theme,
        book_cover=book_cover,
        book_title=book_title,
    )


app.register_blueprint(bp)
app.run(host=os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT", 8080)), debug=True)
