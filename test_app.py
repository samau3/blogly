from models import User, db
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

        User.query.delete()

        user = User(first_name="TestUser", last_name="TestLast", image_url='')
        db.session.add(user)
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
            self.assertIn('<ul>', html)
    
    def test_create_new_user(self):
        """Testing render of user-form"""
        with app.test_client() as client:
      
            resp = client.get('/users/new')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(
                '<form', html)
    
    def test_process_form(self):
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
             