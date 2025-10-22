import os
from unittest import TestCase
from sqlalchemy.exc import IntegrityError
from models import db, User, Artist, UserArtist, Event, UserEvent, WishList, CreateEvent

os.environ['DATABASE_URL'] = "postgresql:///artists_test"

from app import app
app.config['WTF_CSRF_ENABLED'] = False

with app.app_context():
    db.create_all()

class UserModelTestCase(TestCase):
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


    def _sign_up_user(self):
        ''' helper method to sign up a user'''
        
        with app.app_context():
            u = User.signup('Test User', 'TestUsername', 'TestEmail@test.com', 'TestPassword', 'US', '90001', 'Test Bio for user 1', '')

            db.session.add(u)
            db.session.commit()

            u = db.session.query(User).filter_by(username='TestUsername').first()
            return u


    def test_user_model(self):
        ''' Tests commitment to user model table '''

        with app.app_context():
            u = User(
                name='Test Name',
                username='TestUsername',
                email='TestEmail@test.com',
                password='TestPassword',
                country='US',
                zipcode='90001',
                bio='This is a Test Bio',
                profile_img='https://st.depositphotos.com/2101611/3925/v/450/depositphotos_39258143-stock-illustration-businessman-avatar-profile-picture.jpg',
            )

            db.session.add(u)
            db.session.commit()

            self.assertEqual(u.username, 'TestUsername')
            self.assertEqual(u.name, 'Test Name')
            self.assertEqual(u.wishlist.count(), 0)
            self.assertEqual(u.events.count(), 0)
            self.assertEqual(u.artists.count(), 0)


    def test_user_signup(self):
        ''' Tests signup classmethod in user class'''

        with app.app_context():
            u = self._sign_up_user()

            self.assertEqual(u.username, 'TestUsername')

            u = db.session.query(User).filter_by(username='TestUsername').first()

            self.assertIsNotNone(u)

            with self.assertRaises(IntegrityError):
                u = User.signup('Test User2', 'TestUsername', 'TestEmail2@test.com', 'TestPassword', 'US', '90001', 'Test Bio for user 2', '')

                db.session.commit()
            db.session.rollback()

            with self.assertRaises(IntegrityError):
                u = User.signup('Test User3', None, 'TestEmail3@test.com', 'TestPassword', 'US', '90001', 'Test Bio for user 3', '')

                db.session.commit()
            db.session.rollback()


    def test_user_authenticate(self):
        ''' Tests authenticate classmethod in user class'''

        with app.app_context():
            u = self._sign_up_user()

            self.assertEqual(u.username, 'TestUsername')

            u = db.session.query(User).filter_by(username='TestUsername').first()

            self.assertIsNotNone(u)

            u_auth = User.authenticate(u.username, 'TestPassword')

            self.assertTrue(u_auth)
            self.assertEqual(u_auth, u)


    def test_user_update_details(self):
        ''' tests update details class method in user class'''

        with app.app_context():
            u = self._sign_up_user()

            u = db.session.query(User).filter_by(username='TestUsername').first()
            User.update_details(u.id, u.name, 'TestUsernameChange', u.email, u.country, u.zipcode, u.bio)

            db.session.commit()

            u = db.session.query(User).filter_by(username='TestUsernameChange').first()
            self.assertIsNotNone(u)
            self.assertEqual(u.name, 'Test User')


    def test_user_change_password(self):
        '''' tests change password class method on user class'''

        with app.app_context():
            u = self._sign_up_user()

            self.assertEqual(u.username, 'TestUsername')

            u = db.session.query(User).filter_by(username='TestUsername').first()

            self.assertIsNotNone(u)

            pswd_change = User.change_password(u.username, 'NewTestPassword')
            db.session.commit()

            self.assertTrue(pswd_change)

            u_auth = User.authenticate(u.username, 'NewTestPassword')
            self.assertTrue(u_auth)

    
    def test_update_pfp(self):
        ''' tests update profile picture class method in user class'''

        with app.app_context():
            u = self._sign_up_user()

            self.assertEqual(u.username, 'TestUsername')

            u = db.session.query(User).filter_by(username='TestUsername').first()

            self.assertIsNotNone(u)

            pfp_change = User.update_pfp(u.username, 'https://cdn-icons-png.freepik.com/512/8767/8767823.png')
            db.session.commit()

            self.assertTrue(pfp_change)

            u = db.session.query(User).filter_by(username='TestUsername').first()

            self.assertEqual(u.profile_img, 'https://cdn-icons-png.freepik.com/512/8767/8767823.png')


class ArtistModelTestCase(TestCase):
    ''' tests artist model'''

    def setup(self):
        ''' Clears all data '''
        with app.app_context():
            Artist.query.delete()

            db.session.commit()


    def tearDown(self):
        ''' Confirms all data is removed after test runs'''
        with app.app_context():
            Artist.query.delete()

            db.session.commit()


    def test_artist_model(self):
        ''' tests commitment to artist table'''

        with app.app_context():
            artist = Artist(
                name='Test Artist',
                spotify_id='00000000',
                spotify_url='testurl.api/artist',
                image='https://media.istockphoto.com/id/834800606/photo/guitarist-performing-on-stage.jpg?s=612x612&w=0&k=20&c=qV2kb87BO_AYy0258hLiLQM-kBCj9QJ39z_P36ZU0qQ=',
                attraction_id='00000000'
            )

            db.session.add(artist)
            db.session.commit()

            a = db.session.query(Artist).filter_by(name='Test Artist').first()

            self.assertIsNotNone(a)
            self.assertEqual(a.spotify_id, '00000000')

            with self.assertRaises(IntegrityError):
                artist = Artist(
                    name='Test Artist',
                    spotify_id=None,
                    spotify_url='testurl.api/artist2',
                    image='',
                    attraction_id='00000001'
                )
                db.session.add(artist)
                db.session.commit()
            db.session.rollback()


class UserArtistModelTestCase(TestCase):
    ''' Tests the user model '''

    def setup(self):
        ''' Clears all data '''
        with app.app_context():
            User.query.delete()
            Artist.query.delete()
            UserArtist.query.delete()

            db.session.commit()


    def tearDown(self):
        ''' Confirms all data is removed after test runs'''
        with app.app_context():
            User.query.delete()
            Artist.query.delete()
            UserArtist.query.delete()
  
            db.session.commit()


    def test_user_artist_model(self):
        ''' tests commitment to user artist table'''

        with app.app_context():
            u = User(
                name='Test Name',
                username='TestUsername',
                email='TestEmail@test.com',
                password='TestPassword',
                country='US',
                zipcode='90001',
                bio='This is a Test Bio',
                profile_img='https://st.depositphotos.com/2101611/3925/v/450/depositphotos_39258143-stock-illustration-businessman-avatar-profile-picture.jpg',
            )

            a = Artist(
                name='Test Artist',
                spotify_id='00000000',
                spotify_url='testurl.api/artist',
                image='https://media.istockphoto.com/id/834800606/photo/guitarist-performing-on-stage.jpg?s=612x612&w=0&k=20&c=qV2kb87BO_AYy0258hLiLQM-kBCj9QJ39z_P36ZU0qQ=',
                attraction_id='00000000'
            )

            db.session.add_all([u,a])
            db.session.commit()

            ua = UserArtist(
                user_id=u.id, 
                artist_id=a.id
            )

            db.session.add(ua)
            db.session.commit()

            self.assertTrue(ua)
            self.assertEqual(ua.user_id, u.id)

