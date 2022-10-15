import os
import json
import time
import spotipy


def run():
    os.environ['SPOTIPY_CLIENT_ID'] = "b976f3e1bef142b8bce6ae0b9272bca1"
    os.environ['SPOTIPY_CLIENT_SECRET'] = "989927ca5e914b689e577c3578441a45"
    os.environ['SPOTIPY_REDIRECT_URI'] = 'http://localhost:8888/callback'
    # http://localhost:8888/callback

    spotify_client_id = os.environ['SPOTIPY_CLIENT_ID']
    spotify_secret = os.environ['SPOTIPY_CLIENT_SECRET']
    spotify_redirect_uri = os.environ['SPOTIPY_REDIRECT_URI']

    # scope = 'user-read-currently-playing'
    scope = 'user-top-read'
    # scope = 'user-read-recently-played'

    oauth_object = spotipy.SpotifyOAuth(client_id=spotify_client_id,
                                        client_secret=spotify_secret,
                                        redirect_uri=spotify_redirect_uri,
                                        scope=scope)

    # print(oauth_object)

    token_dict = oauth_object.get_access_token()

    token = token_dict['access_token']

    spotify_object = spotipy.Spotify(auth=token)  # auth meaning authentication
    # current = spotify_object.currently_playing()  #The song currently being played
    current = spotify_object.current_user_top_tracks(
        limit=50, offset=0, time_range='short_term')  # The top 50 songs played by the user
    # time_range = 'long_term' my most played songs all time
    # time_range = 'medium_term' my most played songs in the last 6 months
    # time_range = 'short_term' my most played songs in the last 4 weeks

    # current = spotify_object.current_user_top_artists() #The top artists listened by the user
    # current = spotify_object.current_user_recently_played(limit=50)  # The top 50 songs the user recently played

    print(json.dumps(current, indent=4))

    with open('SPOTdata.json', 'w', encoding='utf-8') as f:
        json.dump(current, f, ensure_ascii=False, indent=4)

    print(token)
