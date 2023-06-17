from flask import Flask, request, url_for, session, redirect
from spotipy.oauth2 import SpotifyOAuth
import spotipy
import time
import json

app = Flask(__name__)

app.secret_key = "private"
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
    sp_oauth = create_spotify_oauth()
    session.clear() # clears previous session data
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

    playlists = sp.current_user_playlists() # get user's public playlists

    # Iterate over the playlists and retrieve information
    playlist_list = [] # list with playlists
    for playlist in playlists["items"]:
        playlist_name = playlist["name"]
        playlist_id = playlist["id"]
        playlist_list.append({"name": playlist_name, "id": playlist_id})

    # Prompt user to select playlist to convert
    for index, playlist in enumerate(playlist_list):
        print(f"{index+1}\t{playlist['name']}")

    selection = int(input("Enter the number of the playlist you would like to convert: "))
    
    # Retrieve tracks within the selected playlist
    tracks = sp.playlist_tracks(playlist_list[selection-1]["id"])

    track_list = [] # list with song name and artist
    # Iterate over the tracks and retrieve information
    for item in tracks["items"]:
        track = item["track"]
        track_name = track["name"]
        track_artist = track['artists'][0]['name']
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
        client_id= "private",
        client_secret= "private",
        redirect_uri=url_for("redirectPage", _external=True),
        scope= "user-library-read")