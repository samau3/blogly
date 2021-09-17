from flask import Flask, request, redirect, render_template
from models import connect_db, db, User, Post
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
    return render_template('user-list.html', users=users)


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

    # STORING EMPTY STRING, not getting null

    user = User(
        first_name=first_name,
        last_name=last_name,
        image_url=image_url)

    db.session.add(user)
    db.session.commit()

    return redirect('/users')


@app.get('/users/<int:id>')
def display_user(id):
    """Render data of user, edit and delete button"""

    user = User.query.get_or_404(id)
    return render_template('user-info.html', user=user)


@app.get('/users/<int:id>/edit')
def render_user_edit(id):
    """Render edit page for user"""

    user = User.query.get_or_404(id)
    return render_template('user-edit.html', user=user)


@app.post('/users/<int:id>/edit')
def process_edit_form(id):
    """Process edit form redirect to users page"""

    user = User.query.get_or_404(id)

    user.first_name = request.form['first-name']
    user.last_name = request.form['last-name']
    user.image_url = request.form['image-url']

    db.session.commit()

    return redirect('/users')


@app.post('/users/<int:id>/delete')
def delete_user(id):
    """Delete the current user"""

    user = User.query.get_or_404(id)

    # db.session.delete(user)
    # Loop here delete posts, THEN DELETE user
    
    for post in user.posts_list:
        post.query.delete()
        # db.session.delete(post)

    user.query.delete()
    db.session.commit()
    return redirect('/users')

############################POST ROUTE#############################


@app.get('/users/<int:id>/posts/new')
def render_blog_post_form(id):
    """Find the user id render new post-form"""

    user = User.query.get_or_404(id)

    return render_template('new-post-form.html', user=user)


@app.post('/users/<int:id>/posts/new')
def handle_blog_post_form(id):
    """Create a new instance of Post from the new post form, redirects back to user page"""

    user = User.query.get_or_404(id)

    content = request.form['content']
    title = request.form['title']

    create_new_post = Post(
        title=title,
        content=content,
        user_id=id
    )

    user.posts_list.append(create_new_post)
    db.session.commit()

    return redirect(f'/users/{id}')


@app.get('/posts/<int:id>')
def display_post(id):
    """Render individual post by a user"""

    post = Post.query.get_or_404(id)

    return render_template('post-detail.html', post=post)


@app.get('/posts/<int:id>/edit')
def show_edit_post_form(id):
    """Render edit post form"""

    post = Post.query.get_or_404(id)
    return render_template('edit-post-form.html', post=post)


@app.post('/posts/<int:id>/edit')
def process_post_edit_form(id):
    """Process post edit form, redirect to post detail page"""

    post = Post.query.get_or_404(id)

    post.content = request.form['content']
    post.title = request.form['title']

    db.session.commit()

    return redirect(f'/posts/{id}')


@app.post('/posts/<int:id>/delete')
def delete_post(id):
    """Delete user's post"""

    post = Post.query.get_or_404(id)

    db.session.delete(post)
    db.session.commit()
    return redirect('/users')
