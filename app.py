# Starter code for app.py from Milestone 3.
import flask

app = flask.Flask(__name__)

bp = flask.Blueprint(
    "bp",
    __name__,
    template_folder="./static/react",
)

# Route for serving React page
@bp.route("/")
def index():
    return flask.render_template("index.html")


app.register_blueprint(bp)

app.run()
