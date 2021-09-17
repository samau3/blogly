from models import User, Post, db
from unittest import TestCase
from app import app


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test_db'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class UserTestCase(TestCase):
    """Test User input routes"""

    def setUp(self):
        """Add sample pet."""

        Post.query.delete()
        User.query.delete()

        user = User(first_name="TestUser", last_name="TestLast")
        

        db.session.add(user)
        post = Post(title='Rithm', content='Fuzzy Panda', user_id=user.id)
        user.posts_list.append(post)
       
        db.session.commit()
     
        self.user_id = user.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()


    def test_home_page(self):
        """Testing redirect to user-list"""
        with app.test_client() as client: 
        
            resp = client.get("/")
            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, "http://localhost/users")
    
    def test_users_page(self):
        """Testing render of user-list page"""
        with app.test_client() as client:
      
            resp = client.get('/users')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('TestUser TestLast', html)
    
    def test_create_new_user(self):
        """Testing render of user-form"""
        with app.test_client() as client:
      
            resp = client.get('/users/new')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(
                '<form action="/users/new"', html)
    
    def test_edit_form(self):
        """Testing value forms of new user"""
        with app.test_client() as client: 

            user_data = {"first-name": "TestUser2", "last-name": "TestLast2", "image-url": ''}
            resp = client.post("/users/new", data=user_data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("TestUser2", html)

    def test_user_detail(self):
        """Testing user profile information page"""
        with app.test_client() as client:


            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>TestUser TestLast</h1>', html)
    
    def test_render_blog_post_form(self): 
        """Render form id"""
        with app.test_client() as client:
      
            resp = client.get(f'/users/{self.user_id}/posts/new')
            # breakpoint()
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f'<form action="/users/{self.user_id}/posts/new"', html)

    def test_handle_blog_post_form(self):
        """Testing value forms of new post"""
        with app.test_client() as client: 

            post_data = {"title": "TestUser2", "content": "TestLast2"}
            resp = client.post(f'/users/{self.user_id}/posts/new', data=post_data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("TestUser2", html)
    
    def test_display_post_list(self):
        """Testing render list of post by a user"""
        with app.test_client() as client:

            resp = client.get(f'/posts/{self.user_id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Rithm</h1>', html)

    def test_show_edit_post_form(self):
        """Testing render of edit post form"""
        with app.test_client() as client:

            resp = client.get(f'/posts/{self.user_id}/edit')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f'<form action="/posts/{self.user_id}/edit"', html)