# Note: Be sure to install bcrypt, flask-bcrypt, and flask_wtf (if you haven't already) onto your system.
import os
import flask
import bcrypt
from collections import Counter
from flask import flash, request, render_template
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
    UserForm,
    BookInfoFormAdd,
    BookInfoFormSendRecs,
    BookInfoFormDeleteRecs,
    BookThemeForm,
    BookTitleForm,
    Users,
    Favorites,
    Recommendations,
    Review,
    ReviewForm,
)
from penguin import (
    book_suggestions,
    title_search,
    all_book_info,
    basic_book_info,
    get_single_book_theme,
)

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

bp = flask.Blueprint("bp", __name__, template_folder="./static/react",)

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


# =====================================================================
# SECTION 1: SIGN-UP/LOGIN INFORMATION ROUTES
# =====================================================================
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

        flask.flash("New user successfully registered.")
        return flask.redirect(flask.url_for("login"))

    flask.flash("USER ALREADY EXISTS. PLEASE TRY AGAIN.")
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

    flask.flash("USER DOES NOT EXIST. PLEASE TRY AGAIN.")
    return flask.redirect(flask.url_for("login"))


@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    """Clears the current user's session cookies and redirects you back to the login page."""
    logout_user()
    flask.flash("You have successfully logged out.")
    return flask.redirect(flask.url_for("login"))


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    """Provides the current user with the ability to update their username and email."""
    return_home_button = ReturnHomeButton()
    form = UserForm()
    id = current_user.id
    name_to_update = Users.query.get_or_404(id)
    if request.method == "POST":

        name_to_update.email = request.form["email"]

        name_to_update.username = request.form["username"]
        try:
            db.session.commit()
            flash("User Updated Successfully!")
            return render_template(
                "profile.html",
                form=form,
                name_to_update=name_to_update,
                id=id,
                return_home_button=return_home_button,
            )
        except:
            flash("Error!  Looks like there was a problem...try again!")
            return render_template(
                "profile.html",
                form=form,
                name_to_update=name_to_update,
                id=id,
                return_home_button=return_home_button,
            )
    else:
        return render_template(
            "profile.html",
            form=form,
            name_to_update=name_to_update,
            id=id,
            return_home_button=return_home_button,
        )


# =====================================================================
# SECTION 2: COMMON ROUTES USED FOR PRIMARY APP FEATURES
# =====================================================================
@app.route("/homepage", methods=["GET", "POST"])
@login_required
def homepage():
    """Renders the basic landing page from which most other HTML pages can be reached."""
    logout_button = LogoutButton()
    bookinfo_form_a = BookInfoFormAdd()
    route_name = "homepage"
    display_number = 1

    all_favorites = Favorites.query.filter_by(email=current_user.email).all()
    num_books = len(all_favorites)

    favorite_themes = []
    for i in range(num_books):
        book_theme = get_single_book_theme(all_favorites[i].bookISBN)
        favorite_themes.append(book_theme)

    if num_books != 0:
        occurence_count = Counter(favorite_themes)
        most_common_theme = occurence_count.most_common(1)[0][0]

        # Grabs the second most common theme if the most common theme is "None".
        if most_common_theme == "None":
            most_common_theme = occurence_count.most_common(2)[1][0]

        book_titles, book_urls, book_ISBNs = book_suggestions(
            most_common_theme, display_number
        )
    else:
        book_titles = []
        book_urls = []
        book_ISBNs = []

    return flask.render_template(
        "homepage.html",
        logout_button=logout_button,
        route_name=route_name,
        bookinfo_form_a=bookinfo_form_a,
        book_titles=book_titles,
        book_urls=book_urls,
        book_ISBNs=book_ISBNs,
        num_books=num_books,
        display_number=display_number,
    )


@app.route("/suggestions", methods=["GET", "POST"])
@login_required
def suggestions():
    """Returns the basic suggestions page where books can be suggested to the user based on a chosen theme."""
    return_home_button = ReturnHomeButton()
    theme_form = BookThemeForm()
    bookinfo_form_a = BookInfoFormAdd()
    return flask.render_template(
        "suggestions.html",
        return_home_button=return_home_button,
        theme_form=theme_form,
        bookinfo_form_a=bookinfo_form_a,
    )


@app.route("/handle_theme_suggestions", methods=["GET", "POST"])
@login_required
def handle_theme_suggestions():
    """Based on the theme selected, the titles, ISBNs, and cover images of a random set of books under said theme is returned and rendered on the suggestions page."""
    return_home_button = ReturnHomeButton()
    route_name = "suggestions"
    theme_form = BookThemeForm()
    bookinfo_form_a = BookInfoFormAdd()
    display_number = 6
    if theme_form.validate_on_submit():
        book_titles, book_urls, book_ISBNs = book_suggestions(
            theme_form.theme.data, display_number
        )
        num_books = len(book_titles)
        return flask.render_template(
            "suggestions.html",
            return_home_button=return_home_button,
            route_name=route_name,
            theme_form=theme_form,
            bookinfo_form_a=bookinfo_form_a,
            book_titles=book_titles,
            book_urls=book_urls,
            book_ISBNs=book_ISBNs,
            num_books=num_books,
        )


@app.route("/search_by_title")
@login_required
def search_by_title():
    """Returns the basic search_by_title page where books can be directly searched for using a title input."""
    return_home_button = ReturnHomeButton()
    title_form = BookTitleForm()
    return flask.render_template(
        "search_by_title.html",
        return_home_button=return_home_button,
        title_form=title_form,
    )


@app.route("/handle_title_selection", methods=["GET", "POST"])
@login_required
def handle_title_selection():
    """Returns basic information about a single book based on the provided title input."""
    return_home_button = ReturnHomeButton()
    route_name = "search_by_title"
    title_form = BookTitleForm()
    bookinfo_form_a = BookInfoFormAdd()
    if title_form.validate_on_submit():
        try:
            book_ISBN = title_search(title_form.title.data)
            book_title, book_url = basic_book_info(book_ISBN)
            return flask.render_template(
                "search_by_title.html",
                return_home_button=return_home_button,
                route_name=route_name,
                title_form=title_form,
                bookinfo_form_a=bookinfo_form_a,
                book_title=book_title,
                book_url=book_url,
                book_ISBN=book_ISBN,
                num_books=1,
            )
        except:
            return flask.render_template(
                "search_by_title.html",
                title_form=title_form,
                bookinfo_form_a=bookinfo_form_a,
                return_home_button=return_home_button,
                error=1,
            )


@app.route("/favorites")
@login_required
def favorites():
    """Displays the current user's favorited books on the 'favorites' page."""
    return_home_button = ReturnHomeButton()
    bookinfo_form_srecs = BookInfoFormSendRecs()
    all_favorites = Favorites.query.filter_by(email=current_user.email).all()

    num_books = len(all_favorites)
    book_titles = []
    book_urls = []
    all_favorite_isbns = []

    for i in range(num_books):
        book_title, book_url = basic_book_info(all_favorites[i].bookISBN)
        book_titles.append(book_title)
        book_urls.append(book_url)
        all_favorite_isbns.append(all_favorites[i].bookISBN)

    if num_books == 0:
        return flask.render_template(
            "no_favorites.html", return_home_button=return_home_button,
        )
    else:
        return flask.render_template(
            "favorites.html",
            return_home_button=return_home_button,
            bookinfo_form_srecs=bookinfo_form_srecs,
            book_titles=book_titles,
            book_urls=book_urls,
            book_ISBNs=all_favorite_isbns,
            num_books=num_books,
        )


@app.route("/handle_dualsubmits_add", methods=["POST"])
@login_required
def handle_dualsubmits_add():
    """Based on whether the user wants to explore a book or favorite a book, redirect to proper routes accordingly."""
    bookinfo_form_a = BookInfoFormAdd()
    if bookinfo_form_a.validate_on_submit():
        if bookinfo_form_a.submit_explore.data is True:
            return flask.redirect(
                flask.url_for("get_book_info", isbn=bookinfo_form_a.isbn.data)
            )
        else:
            return flask.redirect(
                flask.url_for(
                    "add_favorite",
                    route=bookinfo_form_a.original_route.data,
                    isbn=bookinfo_form_a.isbn.data,
                )
            )


@app.route("/handle_triple_submits", methods=["POST"])
@login_required
def handle_triple_submits():
    """Based on whether the user wants to explore a book, unfavorite a book, or send a book recommendation, redirect to proper routes accordingly."""
    bookinfo_form_srecs = BookInfoFormSendRecs()
    if bookinfo_form_srecs.validate_on_submit():
        if bookinfo_form_srecs.submit_explore.data is True:
            return flask.redirect(
                flask.url_for("get_book_info", isbn=bookinfo_form_srecs.isbn.data)
            )
        elif bookinfo_form_srecs.submit_delete.data is True:
            return flask.redirect(
                flask.url_for("delete_favorite", isbn=bookinfo_form_srecs.isbn.data,)
            )
        else:
            return flask.redirect(
                flask.url_for(
                    "add_recommendations",
                    isbn=bookinfo_form_srecs.isbn.data,
                    receiver_username=bookinfo_form_srecs.receiver_username.data,
                )
            )


@app.route("/handle_triplesubmits_recdelete", methods=["POST"])
@login_required
def handle_triplesubmits_recdelete():
    """Based on whether the user wants to explore a book, unfavorite a book, or delete a book recommendation from another, redirect to proper routes accordingly."""
    bookinfo_form_drecs = BookInfoFormDeleteRecs()
    if bookinfo_form_drecs.validate_on_submit():
        if bookinfo_form_drecs.submit_explore.data is True:
            return flask.redirect(
                flask.url_for("get_book_info", isbn=bookinfo_form_drecs.isbn.data)
            )
        elif bookinfo_form_drecs.submit_favorite.data is True:
            return flask.redirect(
                flask.url_for(
                    "add_favorite",
                    isbn=bookinfo_form_drecs.isbn.data,
                    route="recommendations",
                )
            )
        else:
            return flask.redirect(
                flask.url_for(
                    "delete_recommendations",
                    isbn=bookinfo_form_drecs.isbn.data,
                    receiver_username=bookinfo_form_drecs.receiver_username.data,
                )
            )


@app.route("/add_favorite")
@login_required
def add_favorite():
    """Adds a valid book ISBN to the favorites list before redirecting the user to the original page from which a book was favorited."""
    original_route = flask.request.args.get("route")
    favorite_isbn = flask.request.args.get("isbn")
    existing_favorite = Favorites.query.filter_by(
        email=current_user.email, bookISBN=favorite_isbn
    ).first()

    if existing_favorite:
        flask.flash("THIS BOOK HAS BEEN FAVORITED ALREADY. PLEASE TRY AGAIN.")
        return flask.redirect(flask.url_for(original_route))

    else:
        new_favorite = Favorites(email=current_user.email, bookISBN=favorite_isbn)
        db.session.add(new_favorite)
        db.session.commit()
        flask.flash("Book has been favorited.")
        return flask.redirect(flask.url_for(original_route))


@app.route("/delete_favorite")
@login_required
def delete_favorite():
    """If found, removes a book from the favorites list before returning the user back to the favorites page."""
    isbn = flask.request.args.get("isbn")
    deleted_book = Favorites.query.filter_by(
        email=current_user.email, bookISBN=isbn
    ).first()
    db.session.delete(deleted_book)
    db.session.commit()
    flask.flash("Book has been unfavorited.")
    return flask.redirect(flask.url_for("favorites"))


@app.route("/recommendations")
@login_required
def recommendations():
    """Displays recommended books sent by other users to the currnent user on the 'recommendations' page."""
    return_home_button = ReturnHomeButton()
    bookinfo_form_drecs = BookInfoFormDeleteRecs()
    all_recommendations = Recommendations.query.filter_by(
        receiverUsername=current_user.username
    ).all()

    num_books = len(all_recommendations)
    book_titles = []
    book_urls = []
    all_recommendations_isbns = []
    recommendation_senders = []

    for i in range(num_books):
        book_title, book_url = basic_book_info(all_recommendations[i].bookISBN)
        book_titles.append(book_title)
        book_urls.append(book_url)
        recommendation_senders.append(all_recommendations[i].senderUsername)
        all_recommendations_isbns.append(all_recommendations[i].bookISBN)

    if num_books == 0:
        return flask.render_template(
            "no_recommendations.html", return_home_button=return_home_button,
        )
    else:
        return flask.render_template(
            "recommendations.html",
            return_home_button=return_home_button,
            bookinfo_form_drecs=bookinfo_form_drecs,
            book_titles=book_titles,
            book_urls=book_urls,
            book_ISBNs=all_recommendations_isbns,
            recommendation_senders=recommendation_senders,
            num_books=num_books,
        )


@app.route("/add_recommendations")
@login_required
def add_recommendations():
    """Adds a valid book ISBN to another user's recommendations list before redirecting the current user to the original page from which a book was recommended."""
    isbn = flask.request.args.get("isbn")
    receiver_username = flask.request.args.get("receiver_username")
    if receiver_username == "":
        flask.flash("A USERNAME MUST BE INPUTTED.")
        return flask.redirect(flask.url_for("favorites"))
    elif receiver_username == current_user.username:
        flask.flash("YOU CANNOT RECOMMEND BOOKS TO YOURSELF. TRY AGAIN.")
        return flask.redirect(flask.url_for("favorites"))

    existing_recommendation = Recommendations.query.filter_by(
        senderUsername=current_user.username,
        receiverUsername=receiver_username,
        bookISBN=isbn,
    ).first()
    user_exists = Users.query.filter_by(username=receiver_username).first()

    if existing_recommendation:
        flask.flash(
            "THIS BOOK HAS BEEN RECOMMENDED TO THIS PERSON ALREADY. PLEASE TRY AGAIN."
        )
        return flask.redirect(flask.url_for("favorites"))
    elif not user_exists:
        flask.flash("THIS USER DOES NOT EXIST. TRY AGAIN.")
        return flask.redirect(flask.url_for("favorites"))
    else:
        new_recommendation = Recommendations(
            senderUsername=current_user.username,
            receiverUsername=receiver_username,
            bookISBN=isbn,
        )
        db.session.add(new_recommendation)
        db.session.commit()
        flask.flash("Book has been recommended.")
        return flask.redirect(flask.url_for("favorites"))


@app.route("/delete_recommendations")
@login_required
def delete_recommendations():
    """If found, removes a book from the current user's recommendations list before returning the user back to the recommendations page."""
    isbn = flask.request.args.get("isbn")
    deleted_book = Recommendations.query.filter_by(
        receiverUsername=current_user.username, bookISBN=isbn
    ).first()
    db.session.delete(deleted_book)
    db.session.commit()
    flask.flash("Book has been un-recommended.")
    return flask.redirect(flask.url_for("recommendations"))


@app.route("/get_book_info", methods=["GET", "POST"])
@login_required
def get_book_info():
    """Displays even more specific info about a book in a separate "bookpage" page based on the provided ISBN."""
    review_form = ReviewForm()
    return_home_button = ReturnHomeButton()
    book_isbn = flask.request.args.get("isbn")
    if book_isbn is None:
        book_isbn = review_form.isbn.data
    isbn_str = str(book_isbn)
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
    review = Review.query.filter_by(isbn=isbn_str).all()
    num_review = len(review)
    if num_review == 0:
        flask.flash("Be the first to add a comment for this book")
    if review_form.validate_on_submit():
        try:
            isbn_str = str(review_form.isbn.data)
            new_review = Review(
                username=current_user.username,
                isbn=isbn_str,
                comment=review_form.comment.data,
                rating=review_form.rating.data,
            )
            db.session.add(new_review)
            db.session.commit()
            new_review = Review.query.filter_by(isbn=isbn_str).all()
            new_num_review = len(new_review)
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
                review=new_review,
                num_review=new_num_review,
                review_form=review_form,
                return_home_button=return_home_button,
            )
        except ValueError:
            flask.flash("Something went wrong")
            return flask.render_temlate(
                "bookpage.html",
                author=author,
                flapcopy=flapcopy,
                author_bio=author_bio,
                book_isbn=book_isbn,
                page_num=page_num,
                book_theme=book_theme,
                book_cover=book_cover,
                book_title=book_title,
                review_form=review_form,
                return_home_button=return_home_button,
            )
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
        review=review,
        num_review=num_review,
        review_form=review_form,
        return_home_button=return_home_button,
    )


app.register_blueprint(bp)
app.run(host=os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT", 8080)), debug=True)
