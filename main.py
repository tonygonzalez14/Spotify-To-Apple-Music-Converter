import subprocess
import os
import time

# Run the Spotify API Flask app
subprocess.run(['python', 'app.py'])

# Wait for the JSON file to be created
json_file_path = 'C:\\Users\\tonyg\\OneDrive\\Desktop\\Playlist Creator Project\\track_data.json'

while not os.path.exists(json_file_path):
    time.sleep(1) # wait for 1 second before checking again

# Terminate the Flask app subprocess and close the current browser window
flask_app_process.terminate()
os.system("taskkill /im chrome.exe /f")

# Run the Apple Music script
subprocess.run(['python', 'apple_music_driver.py'])

# Run the Music Recommender script
subprocess.run(['python', 'new_music_recommender.py'])

# Delete the JSON file
if os.path.exists(json_file_path):
    os.remove(json_file_path)
