from flask import Flask, request, redirect, render_template
from models import connect_db, db, User
from flask_debugtoolbar import DebugToolbarExtension


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


@app.get('/')
def home_page():
    """At the moment, redirects to /users page"""

    return redirect('/users')

@app.get('/users')
def users_page():
    """List users and show add form"""
    # access the database for users; pass this into html
    # creates links for the user information
    # also has a link to add users

    users = User.query.all()
    return render_template('user-list.html', users = users)


# Create html form w/ method of POST
# Need a form of method with three inputs, button

@app.get('/users/new')
def create_new_user():
    """Show add form for users"""


    return render_template('user-form.html')

@app.post('/users/new')
def process_form():
    """Process form and add new user"""

    first_name = request.form['first-name']
    last_name = request.form['last-name']
    image_url = request.form['image-url'] 

    image_url = image_url if image_url else None

    user = User(
        first_name = first_name, 
        last_name = last_name, 
        image_url = image_url)

    db.session.add(user)
    db.session.commit()

    return redirect('/users')

# FIXME: bug error while rendering invalid maluser 
# @app.get('/users/<int:user-id>')
# def display_user():
#     # Play user-id in parameter
#     """Render data of user, edit and delete button"""

#     return render_template('/')

# @app.get('/users/<int:user-id>/edit')
# def render_user_edit():
#     """Render edit page for user"""

#     return render_template('/')

# @app.post('/users/<int:user-id>/edit')
# def process_edit_form():
#     """Process edit form redirect to users page"""

#     return redirect('/users')

# @app.post('/users/<int:id>/delete')
# def delete_user():
#     """Delete the current user"""
#     return redirect('/users')