import base64
import time
import requests
from urllib.parse import urlencode


class SpotifyAPI:
    ''' class to handle all spotify functions '''

    def __init__(self, client_id, client_secret, redirect_uri, base_url="https://api.spotify.com/v1", token_url='https://accounts.spotify.com/api/token', auth_url='https://accounts.spotify.com/authorize', scope='user-read-private user-read-email user-top-read streaming'):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.base_url = base_url
        self.token_url = token_url
        self.auth_url = auth_url
        self.scope = scope


# TOKENS/ GENERIC SPOTIFY API

    def auth_token_header(self):
        ''' creates the header for auth '''

            # combines client id and client secret 
        auth_str = f'{self.client_id}:{self.client_secret}'
            # converts str to bytes
        auth_bytes = auth_str.encode('utf-8')
            # converts to binary and decodes it from byte back to string
        auth_base64 = base64.b64encode(auth_bytes).decode('utf-8')
        return {'Authorization': f'Basic {auth_base64}'}


    def get_token(self, code):
        ''' gets a token with a provided Spotify code and returns token info'''

        payload = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': self.redirect_uri
        }

        headers = self.auth_token_header()

        res = requests.post(self.token_url, data=payload, headers=headers)

        return res.json()


    def refresh_token(self, refresh_token):
        ''' refreshes token and returns refreshed token info'''

        payload = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token
        }

        headers = self.auth_token_header()

        res = requests.post(self.token_url, data=payload, headers=headers)

        return res.json()    


    def check_refesh_get_token(self, token_info=None):
        ''' takes in token info and checks if token is expired. if token is expired, returns a new one'''

        info = token_info

        if info:
                # checks if token expire time is less than current time (both in seconds)
            if info['expires_at'] < int(time.time()):
                    # refreshes token if needed
                info = self.refresh_token(info['refresh_token'])
                if info:
                        # updates expiration time
                    info['expires_at'] = int(time.time() + info['expires_in'])
                return None
        return info['access_token']
    
    
    def callback(self, code):
        ''' takes in a code to use to get token info, returns token info'''

            # gets token info from code
        if code:
            token_info = self.get_token(code)
            if token_info:
                    # creates expires time
                token_info['expires_at'] = int(time.time() + token_info['expires_in'])
                return token_info
            return None
        return None
    

# FUNCTIONS


    def swtich_account(self):
        ''' switches connected spotify account'''

            # creates url to switch linked spotify account
        params = {
            'client_id': self.client_id,
            'scope': self.scope,
            'response_type': 'code',
            'redirect_uri': self.redirect_uri,
            'show_dialog': True
        }
        return f'{self.auth_url}?{urlencode(params)}'


    def login_with_spotify(self, token_info=None):
        ''' takes in token info and logins in to spotify, returns link to authenticate'''

            # creates auth url
        if token_info == None:
            params = {
                'client_id': self.client_id,
                'scope': self.scope,
                'response_type': 'code',
                'redirect_uri': self.redirect_uri,
            }

            return f'{self.auth_url}?{urlencode(params)}'


    def get_cur_u(self, headers):
        ''' returns information on currently logged in user'''

            # requests user information
        res = requests.get(f'{self.base_url}/me', headers=headers)
        return res.json()


    def get_cur_u_top_artists(self, headers):
        ''' gets the users top artists '''

            # requests top 10 artists data
        top_artists = requests.get(
            f'{self.base_url}/me/top/artists',
            params={
                'limit': 10,
                'time_range': 'long_term'
            },
            headers=headers
        )

        users_top = top_artists.json()

        artists_setup = []

            # finds the image with the biggest resolution
        for artist in users_top.get('items', {}):
            images = artist.get('images')
            cur_biggest = 0
            for image in images:
                if int(image.get('width', 0)) >= cur_biggest:
                    cur_biggest = int(image.get('width', 0))
                    image_url = image.get('url', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTwoFiJiFNFd9HI4Ez177ayXT1aDEejtgyMJA&s')
                else:
                    continue

                    # parses data from spotify
            setup = {
                'name': artist.get('name', None),
                'spotify_id': artist.get('id'),
                'spotify_url': artist.get('external_urls', {}).get('spotify', None),
                'image_url': image_url
            }
            artists_setup.append(setup)     

        return artists_setup if artists_setup else None


    def get_cur_u_top_tracks(self, headers):
        ''' gets the users top tracks'''

            # requests top 3 tracks data
        top_tracks = requests.get(
            f'{self.base_url}/me/top/tracks',
            params={
                'limit': 3,
                'time_range': 'long_term'
            },
            headers=headers
        )

        users_top = top_tracks.json()

        track_setup = []

            # finds the image with the biggest resolution 
        for track in users_top.get('items', {}):
            images = track.get('album', {}).get('images')
            cur_biggest = 0
            for image in images:
                if int(image.get('width', 0)) >= cur_biggest:
                    cur_biggest = int(image.get('width', 0))
                    image_url = image.get('url', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTwoFiJiFNFd9HI4Ez177ayXT1aDEejtgyMJA&s')
                else:
                    continue

                    # parses data from spotify
            setup = {
                'name': track.get('album', {}).get('name', None),
                'artist': track.get('album', {}).get('artists',[])[0].get('name', None),
                'image_url': image_url
            }
            track_setup.append(setup)     

        return track_setup if track_setup else None
