The Spotify to Apple Music Playlist Converter is a Python program that automates the process of transferring playlists from Spotify to Apple Music. The program leverages the Spotify API to retrieve track information and perform the conversion. The program also utilizes the Selenium framework for web browser automation, allowing it to interact with the Apple Music web interface. It provides an automated solution, eliminating the need for manual song searching and adding, and streamlining the process of playlist conversion.

The program consists of three main components:

Spotify API Flask App: This component interacts with the Spotify API to authenticate the user, retrieve the track data from a selected Spotify playlist, and save it as a JSON file. The Flask app utilizes the Spotipy library to simplify communication with the Spotify API.

Apple Music Script: The Apple Music Playlist Automation Script utilizes the Selenium framework for web browser automation to seamlessly add songs from the track_data JSON file to a new playlist on Apple Music. 

Script Runner: Runs the Spotify API Flask app, waits for the JSON file containing the track data, executes the Apple Music script to add the tracks to a new playlist, terminates the Flask app subprocess, and deletes the JSON file.
