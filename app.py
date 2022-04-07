import flask
import os
from penguin import book_search
from models import SignupForm, LoginForm, Users, Favorites
app = flask.Flask(__name__)

bp = flask.Blueprint(
    "bp",
    __name__,
    template_folder="./static/react",
)

@app.route('/login', methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Signup.query.filter_by(
            email=form.email.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)  
                return redirect(url_for('homepage'))

    return render_template('login.html', form= form)
    #no login.html page as of now



@app.route('/signup', methods=["GET","POST"])
def signup():
    form= SignupForm()

    if form.validate_on_submit(): 
       hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
       new_user = Signup(email=form.email.data ,password=hashed_password)
       db.session.add(new_user)
       db.session.commit()
       
       return redirect(url_for('login'))

    return render_template( "signup.html", form = form)
    #no signup.html page 


@app.route('/logout', methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
    #no login page yet
db = SQLAlchemy()


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
@bp.route("/")
def index():
    return flask.render_template("index.html")


app.register_blueprint(bp)

app.run(host=os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT", 8080)), debug=True)
