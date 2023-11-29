from unittest import TestCase
from app import app
from flask import session
from models import db , User 
import json

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all();

class FlaskTests(TestCase):
    """Clean any existing Users"""

    def setUp(self):
        User.query.delete()
        user =User(first_name ="Giovanny",last_name="Bejarano",image="https://www.google.com/url?sa=i&url=https%3A%2F%2Funsplash.com%2Fs%2Fphotos%2Fmen&psig=AOvVaw3IeqUj8WebhlWBpOEc-r6S&ust=1701300564336000&source=images&cd=vfe&ved=0CBEQjRxqFwoTCPDZvNDs54IDFQAAAAAdAAAAABAE")
        db.session.add(user)
        db.session.commit()
        self.user_id = user.id

    def tearDown(self):
        db.session.rollback()

    def test_home_page(self):
      with app.test_client() as client:
        resp = client.get("/")
        html = resp.get_data(as_text=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('<h1>Users</h1>', html)

    
    def test_show_user(self):
      with app.test_client() as client:
        resp = client.get(f"/showuser/{self.user_id}")
        html = resp.get_data(as_text=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('<h1>User Detail</h1>', html)

    def test_update_user(self):
        with app.test_client() as client:
          
            d = {"first_name":"Giovanny", "last_name":"Hamon","image":"https://www.google.com/url?sa=i&url=https%3A%2F%2Funsplash.com%2Fs%2Fphotos%2Fmen&psig=AOvVaw3IeqUj8WebhlWBpOEc-r6S&ust=1701300564336000&source=images&cd=vfe&ved=0CBEQjRxqFwoTCPDZvNDs54IDFQAAAAAdAAAAABAE"}
            resp = client.post(f"/update/{self.user_id}", data=d)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Hamon", html)


    def test_add_user(self):
      with app.test_client() as client:

        d = {"first_name":"Miranda", "last_name":"Hamon","image":"https://www.google.com/url?sa=i&url=https%3A%2F%2Funsplash.com%2Fs%2Fphotos%2Fmen&psig=AOvVaw3IeqUj8WebhlWBpOEc-r6S&ust=1701300564336000&source=images&cd=vfe&ved=0CBEQjRxqFwoTCPDZvNDs54IDFQAAAAAdAAAAABAE"}
        resp = client.post("/createuser", data=d, follow_redirects=True)
        html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn("Miranda", html)

    