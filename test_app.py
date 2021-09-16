from models import User 
from unittest import TestCase
from app import app

app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

class UserTestCase(TestCase):
    """Test User input routes"""

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

            resp = client.post('/users/new', data = {'first-name': 'Dave', 'last-name': 'Baxter', 'image-url': ''})

        
            first_name = resp['first-name']
            last_name = resp['last-name']
            image_url = resp['image-url']

            #html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(type(first_name), str)
            self.assertEqual(type(last_name), str)
            self.assertEqual(type(image_url), str)


             
             