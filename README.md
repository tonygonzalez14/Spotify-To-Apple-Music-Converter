The Spotify to Apple Music Playlist Converter is a Python program that automates the process of transferring playlists from Spotify to Apple Music. The program leverages the Spotify API to retrieve track information and perform the conversion. The program also utilizes the Selenium framework for web browser automation, allowing it to interact with the Apple Music web interface. It provides an automated solution, eliminating the need for manual song searching and adding, and streamlining the process of playlist conversion.

The program consists of three main components:

Spotify API Flask App: This component interacts with the Spotify API to authenticate the user, retrieve the track data from a selected Spotify playlist, and save it as a JSON file. The Flask app utilizes the Spotipy library to simplify communication with the Spotify API.

Apple Music Script: The Apple Music Playlist Automation Script utilizes the Selenium framework for web browser automation to seamlessly add songs from the track_data JSON file to a new playlist on Apple Music. 

Main Script Driver: Runs the Spotify API Flask app, waits for the JSON file containing the track data, executes the Apple Music script to add the tracks to a new playlist, terminates the Flask app subprocess, and deletes the JSON file.

How the program works:

1. The program starts a Flask app that interacts with the Spotify API. The user is prompted to log in to their Spotify account and authorize the app.

2. Once authorized, the Flask app retrieves the user-selected Spotify playlist's track information using the Spotify API. The track data, including the track name and artist, is stored in a JSON file.

3. The program then uses the Selenium framework to automate web browser interaction. It opens the Apple Music web interface in a browser window.

4. The user provides their Apple Music credentials, allowing the program to access their Apple Music account.

5. Using the obtained track data from the Spotify API, the program searches for each track on the Apple Music web interface using browser automation.

6. When an identical track is found on Apple Music, the program adds it to a new playlist on the user's Apple Music account using the browser automation capabilities.

Once all the tracks are added, the playlist conversion process is complete.
