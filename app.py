from flask import Flask, render_template, request, jsonify
import spotipy
import os
import json
import time


app = Flask(__name__)


@app.route("/")
@app.route("/home")
def home():
    return render_template('index.html')


@app.route("/result", methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        name = request.form['name']
        os.environ['SPOTIPY_CLIENT_ID'] = "XXXXXXXXXXXXX"
        os.environ['SPOTIPY_CLIENT_SECRET'] = "YYYYYYYYYYYYY"
        os.environ['SPOTIPY_REDIRECT_URI'] = 'http://localhost:8888/callback'

        spotify_client_id = os.environ['SPOTIPY_CLIENT_ID']
        spotify_secret = os.environ['SPOTIPY_CLIENT_SECRET']
        spotify_redirect_uri = os.environ['SPOTIPY_REDIRECT_URI']

        scope = 'user-top-read'

        oauth_object = spotipy.SpotifyOAuth(client_id=spotify_client_id,
                                            client_secret=spotify_secret,
                                            redirect_uri=spotify_redirect_uri,
                                            scope=scope)

        token_dict = oauth_object.get_access_token()

        token = token_dict['access_token']

        spotify_object = spotipy.Spotify(
            auth=token)  # auth meaning authentication
        current = spotify_object.current_user_top_tracks(
            limit=10, offset=0, time_range='short_term')  # The top 50 songs played by the user

        with open('SPOTdata.json', 'w', encoding='utf-8') as f:
            json.dump(current, f, ensure_ascii=False, indent=4)

        songs_list = []
        f = open('SPOTdata.json',)
        songs_data = json.load(f)
        for i in songs_data['items']:
            songs_list.append(i['name'])

        return render_template('random.html', List=songs_list)


# Initiating the application
if __name__ == '__main__':
    app.run(debug=True)
