import os
from unittest import TestCase
from models import db, User, Artist, UserArtist, Event, UserEvent, WishList, CreateEvent

os.environ['DATABASE_URL'] = "postgresql:///artists_test"

from app import app
app.config['WTF_CSRF_ENABLED'] = False

with app.app_context():
    db.create_all()


class ViewsTestCase(TestCase):
    ''' Tests the user model '''

    def setUp(self):
        ''' Clears all data '''
        with app.app_context():
            User.query.delete()
            Artist.query.delete()
            UserArtist.query.delete()
            Event.query.delete()
            UserEvent.query.delete()
            WishList.query.delete()

            db.session.commit()

            self.client = app.test_client()

            self.username = 'TestUsername'
            self.password = 'TestPassword'


    def tearDown(self):
        ''' Confirms all data is removed after test runs'''
        with app.app_context():
            User.query.delete()
            Artist.query.delete()
            UserArtist.query.delete()
            Event.query.delete()
            UserEvent.query.delete()
            WishList.query.delete()

            db.session.commit()


    def _signup_login_user(self, client):
        ''' helper method to sign up and login a user'''

        u_data = {'name': 'Test Name', 'username': self.username, 'email': 'TestEmail@test.com', 'password': self.password, 'country': 'United States of America', 'zipcode': '90001', 'bio': 'test bio', 'profile_img': ''}

        login_data = {'username': 'Test Name', 'password':'TestPassword'}

        signup = client.post('/signup', data=u_data, follow_redirects=False)
        self.assertEqual(signup.status_code, 302)

        login = client.post('/login', data=login_data, follow_redirects=False)
        self.assertEqual(login.status_code, 302)

        u = db.session.query(User).filter_by(username='TestUsername').first()

        return u


    def test_homepage(self):
        ''' tests homepage without a logged in user'''

        with app.app_context():
            res = self.client.get('/')
            html = res.get_data(as_text=True)

            self.assertIn('Hello, you should login for a personal experience', html)


    def test_homepage_with_user(self):
        ''' tests homepage with a logged in user '''

        with app.app_context():
            u = self._signup_login_user(self.client)

            self.assertIsNotNone(u)

            res = self.client.get('/')
            html = res.get_data(as_text=True)

            self.assertIn('(Connect Spotify to See)', html)


    def test_homepage_with_spotify_login(self):
        ''' tests homepage with a logged in user and a connected spotify account'''

        with app.app_context():
            u = self._signup_login_user(self.client)

            a1 = Artist(name='artist1', spotify_id='00000', spotify_url='http://example.com/artist1', image='http://example.com/artist1.jpg', attraction_id='00000')

            a2 = Artist(name='artist2', spotify_id='00001', spotify_url='http://example.com/artist2', image='http://example.com/artist2.jpg', attraction_id='00001')

            db.session.add_all([a1,a2])
            db.session.commit()

            with self.client.session_transaction() as sess:
                sess['spotify_token'] = 'test_spotify_token'
                sess['top_tracks'] = [
                    {'name': 'track1', 'artist': 'artist1', 'image_url': 'http://example.com/track1.jpg'},
                    {'name': 'track2', 'artist': 'artist2', 'image_url': 'http://example.com/track2.jpg'}
                ]

            res = self.client.get('/')
            html = res.get_data(as_text=True)

            self.assertIn('artist1', html)


    def test_edit_user_details_GET(self):
        ''' test getting the edit details page'''

        with app.app_context():
            u = self._signup_login_user(self.client)

            res = self.client.get(f'/user/details/edit/{self.username}')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1>Edit Details</h1>', html)


    def test_edit_user_details_POST(self):
        ''' test updating a users profile'''

        with app.app_context():
            u = self._signup_login_user(self.client)

            edit_data = {'name': 'Test Name', 'username': 'TestUsernameChange', 'email': 'TestEmail@test.com', 'password': self.password, 'country': 'United States of America', 'zipcode': '90001', 'bio': 'test bio'}

            res = self.client.post('/user/details/edit/TestUsername', data=edit_data)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('TestUsernameChange', html)


    def test_change_password_GET(self):
        ''' test getting the edit details page'''

        with app.app_context():
            u = self._signup_login_user(self.client)

            res = self.client.get(f'/user/password/edit/{self.username}')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<title>Change Password</title>', html)


    def test_change_password_POST(self):
        ''' test getting the edit details page'''

        with app.app_context():
            u = self._signup_login_user(self.client)

            pswd_data = {'password': self.password, 'new_password': 'ChangePassword'}

            res = self.client.post(f'/user/password/edit/{self.username}', data=pswd_data)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn(self.username, html)


    def test_add_to_wishlist(self):
        ''' test adding an event to wishlist'''

        with app.app_context():
            u = self._signup_login_user(self.client)

            e = Event(event_id='00000', name='test event', artist='artist1', url='http://example.com/event', image='http://example.com/event.jpg', date='2025-12-01', location='Los Angeles, California')
            db.session.add(e)
            db.session.commit()

            res = self.client.post(f'/add-to-wishlist/{e.event_id}')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('event added to wishlist', html)


    def test_remove_from_wishlist(self):
        ''' test removing an event to wishlist'''

        with app.app_context():
            u = self._signup_login_user(self.client)

            e = Event(event_id='00000', name='test event', artist='artist1', url='http://example.com/event', image='http://example.com/event.jpg', date='2025-12-01', location='Los Angeles, California')
            db.session.add(e)
            db.session.commit()

            wishlist = WishList(user_id=u.id, event_id=e.event_id)
            db.session.add(wishlist)
            db.session.commit()

            res = self.client.post(f'/remove-wishlist/{e.event_id}')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('event removed from wishlist', html)


    def test_logout(self):
        ''' test logging out of account'''

        with app.app_context():
            u = self._signup_login_user(self.client)

            res = self.client.get('/logout', follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('Hello, you should login for a personal experience', html)       