from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import json

# Iterates through track_data JSON file and adds all songs to new Apple Music Playlist
def add_songs_to_playlist(driver, track_data, wait):
    missed_songs = []
    search_field = driver.find_element(By.XPATH, "//*[@id='search-input-form']/input") # find search field
    # Search for songs and add to new playlist
    for track_info in track_data:
        time.sleep(0.5) # wait for previous song to be added
        search_field.clear()
        search_field.send_keys(track_info["name"] + " " + track_info["artist"], Keys.ENTER)
        time.sleep(0.5) # wait for new song to load
        
        try:
            options_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='scrollable-page']/main/div/div[3]/div[4]/div/div[2]/section/div[1]/ul/li[1]/div/div/div[2]/div/amp-contextual-menu-button/button")))
            options_button.click() # open options nested box
            
            add_playlist_button = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/amp-contextual-menu/div/div/ul/amp-contextual-menu-item[1]/li/button")))
            add_playlist_button.click() # open playlists nested box
            
            current_playlist_button = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/amp-contextual-menu/div/div/ul/amp-contextual-menu-item[1]/li/div/amp-contextual-menu/div/div/ul/amp-contextual-menu-item[2]/li")))
            current_playlist_button.click() # add to playlist      
            
            print(f"{track_info['name']} by {track_info['artist']} added")
        except: # if song could not be found
            print(f"{track_info['name']} by {track_info['artist']} not added")
            missed_songs.append(f"{track_info['name']} by {track_info['artist']}") # add to missed songs list
            
    print("Conversion Complete")
    if missed_songs: # print songs not converted
        print("Songs not converted:", missed_songs)

def main():
    # Keep website window open 
    options = Options()
    options.add_experimental_option("detach", False)

    # Open existing user's Chrome browser
    options.add_argument("--user-data-dir=C:\\Users\\tonyg\\AppData\\Local\\Google\\Chrome\\User Data")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                            options=options)

    # Open website and maximize window
    driver.get("https://music.apple.com/us/listen-now?l=en-US")
    driver.maximize_window()

    # Wait until site loads, if already signed in, begin conversion, else, have user log in
    wait = WebDriverWait(driver, timeout=3600)
    login_success = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='navigation']/div[3]/div[3]/ul/li[1]/a")))
    if login_success:
        print("Login successful...")
    time.sleep(3) # wait for site to load

    # Open track data for reading
    with open('track_data.json', 'r') as file:
        track_data = json.load(file)
    
    wait = WebDriverWait(driver, timeout=3)
    add_songs_to_playlist(driver, track_data, wait) # add songs to playlist
    
if __name__ == "__main__":
    main()
