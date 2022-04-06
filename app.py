# Starter code for app.py from Milestone 3.
import flask
import os

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

app.run(host=os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT", 8080)), debug=True)
