import bcrypt
from flask import redirect, render_template, url_for
import os
from app import app
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user
from wtforms import StringField, SubmitField, PasswordField
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt


db = SQLAlchemy(app)
bcrypt = Bcrypt(app)



login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view ="login"


@login_manager.user_loader
def load_user(user_id):
    return Signup.query.get(int(user_id))

class Signup(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email= db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)

db.create_all()

class SignupForm(FlaskForm):

    email =StringField(validators=[InputRequired(), Length(
        min=1, max =64)], render_kw={"placeholder": "Email"})

    username =StringField(validators=[InputRequired(), Length(
        min=1, max =15)], render_kw={"placeholder": "Username"})

    password =PasswordField(validators=[InputRequired(), Length(
        min=2, max =10)], render_kw={"placeholder": "Password"})

    submit = SubmitField("Sign Up")

    def validate_email(self, email):
        existing_email = Signup.query.filter_by(
            email=email.data).first()

        if existing_email:
            raise ValidationError(
                "That email already exists."
            )

    def validate_username(self, username):
        existing_username = Signup.query.filter_by(
            username=username.data).first()

        if existing_username:
            raise ValidationError(
                "That Username already exists."
            )


class LoginForm(FlaskForm):

    email =StringField(validators=[InputRequired(), Length(
        min=2, max =10)], render_kw={"placeholder": "Email"})

    submit = SubmitField("Login")

    password =PasswordField(validators=[InputRequired(), Length(
        min=2, max =10)], render_kw={"placeholder": "Password"})


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