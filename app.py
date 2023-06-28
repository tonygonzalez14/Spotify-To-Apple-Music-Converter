from flask import Flask, request, url_for, session, redirect
from spotipy.oauth2 import SpotifyOAuth
import spotipy
import time
import json

app = Flask(__name__)

app.secret_key = "JAISJd1238nfMA"
app.config["SESSION_COOKIE_NAME"] = "App Cookie"
TOKEN_INFO = "token_info"

# Prompt user to login to access user data
@app.route('/') 
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

# Redirect after authentication success or failure
@app.route('/redirect')
def redirectPage():
    session.clear() # clears previous session data
    sp_oauth = create_spotify_oauth()
    code = request.args.get("code")
    token_info = sp_oauth.get_access_token(code) # generates token
    session[TOKEN_INFO] = token_info
    return redirect(url_for("getTracks", _external=True))

# Get tracks from playlist
@app.route('/getTracks')
def getTracks():
    try: # user is logged in
        token_info = get_token()
    except: # user is not logged in, redirect to login page
        print("User not logged in")
        return redirect(url_for("login", _external=False))

    sp = spotipy.Spotify(auth=token_info["access_token"])

    # Get user's playlists
    playlists = []
    offset = 0
    while True:
        response = sp.current_user_playlists(limit=50, offset=offset)
        items = response["items"]
        playlists.extend(items)
        offset += len(items)
        if not response["next"]:
            break

    # Iterate over the playlists and retrieve information
    playlist_list = []  # list with playlists
    for playlist in playlists:
        playlist_name = playlist["name"]
        playlist_id = playlist["id"]
        playlist_list.append({"name": playlist_name, "id": playlist_id})

    # Prompt user to select playlist to convert
    for index, playlist in enumerate(playlist_list):
        print(f"{index+1}\t{playlist['name']}")

    selection = int(input("Enter the number of the playlist you would like to convert: "))

    # Retrieve tracks within the selected playlist
    playlist_id = playlist_list[selection-1]["id"]
    tracks = []
    offset = 0
    while True:
        response = sp.playlist_tracks(playlist_id, offset=offset)
        items = response["items"]
        tracks.extend(items)
        offset += len(items)
        if not response["next"]:
            break

    # Iterate over the tracks and retrieve information
    track_list = []  # list with song names and artists
    for item in tracks:
        track = item["track"]
        track_name = track["name"]
        track_artist = track["artists"][0]["name"]
        track_list.append({"name": track_name, "artist": track_artist})

    # Open a file for writing
    with open('track_data.json', 'w') as file:
        # Write the track data to the file in JSON format
        json.dump(track_list, file)

    return str(track_list)

# Checks if current token is expired, generates a new one if so
def get_token():
    token_info = session.get(TOKEN_INFO, None)
    if not token_info: # raises exception if user is not logged in
        raise "exception"
    now = int(time.time())
    is_expired = token_info['expires_at'] - now < 60
    if (is_expired): # checks if current token is expired
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(token_info["refresh_token"])
    return token_info

# OAuth object for API access
def create_spotify_oauth():
    return SpotifyOAuth(
        client_id= "ecf863c62fd947c2aa1e7a8b72610285",
        client_secret= "ea7f27e6d1924babac722786aa092ffa",
        redirect_uri=url_for("redirectPage", _external=True),
        scope= "user-library-read playlist-read-private playlist-read-collaborative")
