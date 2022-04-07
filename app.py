# Starter code for app.py from Milestone 3.
import flask
import os
from penguin import book_search

app = flask.Flask(__name__)
bp = flask.Blueprint("bp", __name__, template_folder="./static/react",)


@app.route("/handle_theme_suggestions")
def handle_theme_suggestions():
    """Based on the theme selected, the title and cover image of a random book under said theme is returned and rendered in a webpage."""
    data = flask.request.form
    book_title, img_url = book_search(data["theme"])
    return flask.render_template(
        # At the time of writing this (4/05), no homepage.html webpage currently exists. This is just a placeholder for now.
        "homepage.html",
        book_title=book_title,
        img_url=img_url,
    )


# Route for serving React page
@bp.route("/getbook")
def getbook():
    return flask.render_template("index.html")


app.register_blueprint(bp)

app.run(host=os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT", 8080)), debug=True)
