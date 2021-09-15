from flask import Flask, request, redirect, render_template
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///sqla_intro'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)


app.get('/')
def home_page():
    """At the moment, redirects to /users page"""

    return redirect('/users')

app.get('/users')
def users_page():
    """List users and show add form"""
    # access the database for users; pass this into html
    # creates links for the user information
    # also has a link to add users

    users = User.query.all()

    return render_template("", users = users)