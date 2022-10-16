from flask import Flask, render_template, request, jsonify
import spotipy
import os
import json
import time
# import spot.py  # from spot.py import run
List = ['1', '2', '3']

app = Flask(__name__)


# @app.route("/")
# @app.route("/login")
# def login():
#     return render_template('index.html')
@app.route("/")
@app.route("/home")
def home():
    return render_template('index.html')


# @app.route("/result", methods=['POST', 'GET'])
@app.route("/result", methods=['POST', 'GET'])
def result():
    # if request.method == 'GET':
    if request.method == 'POST':
        name = request.form['name']
        # if request.form['submit_button'] == 'button1':
        #     # output = request.form.to_dict()
        #     # name = output["name"]
        #     return render_template("info.html", name=name)  # , name=name)
        # elif request.form['submit_button'] == 'button2':
        #     return render_template("random.html", List=List)
    # elif request.method == 'POST':
        os.environ['SPOTIPY_CLIENT_ID'] = "XXXXXXXXXXXXX"
        os.environ['SPOTIPY_CLIENT_SECRET'] = "YYYYYYYYYYYYY"
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

        spotify_object = spotipy.Spotify(
            auth=token)  # auth meaning authentication
        # current = spotify_object.currently_playing()  #The song currently being played
        current = spotify_object.current_user_top_tracks(
            limit=10, offset=0, time_range='short_term')  # The top 50 songs played by the user
        # time_range = 'long_term' my most played songs all time
        # time_range = 'medium_term' my most played songs in the last 6 months
        # time_range = 'short_term' my most played songs in the last 4 weeks

        # current = spotify_object.current_user_top_artists() #The top artists listened by the user
        # current = spotify_object.current_user_recently_played(limit=50)  # The top 50 songs the user recently played

        # print(json.dumps(current, indent=4))

        with open('SPOTdata.json', 'w', encoding='utf-8') as f:
            json.dump(current, f, ensure_ascii=False, indent=4)

        songs_list = []
        f = open('SPOTdata.json',)
        songs_data = json.load(f)
        for i in songs_data['items']:
            songs_list.append(i['name'])
            # for song in i['name']:
            # print(song)

        # print(token)

        # return jsonify(current)  # json.dumps(current, indent=4)
        # return songs_list
        return render_template('random.html', List=songs_list)


# Initiating the application
if __name__ == '__main__':
    app.run(debug=True)
