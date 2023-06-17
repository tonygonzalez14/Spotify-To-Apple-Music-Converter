import subprocess
import os
import time

# Run the Spotify API Flask app
flask_app_process = subprocess.Popen(['flask', 'run'])

# Wait for the JSON file to be created
json_file_path = 'C:\\Users\\tonyg\\OneDrive\\Desktop\\Playlist Creator Project\\track_data.json'

while not os.path.exists(json_file_path):
    time.sleep(1) # wait for 1 second before checking again

# Run the Apple Music script
subprocess.run(['python', 'appleMusicRunner.py'])

# Terminate the Flask app subprocess
flask_app_process.terminate()

# Delete the JSON file
if os.path.exists(json_file_path):
    os.remove(json_file_path)