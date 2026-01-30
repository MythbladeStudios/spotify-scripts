# Author: MythbladeStudios
# Date Created: 10-31-2025
# Description: Converts a spotify playlist into a txt file which you can use 
# with another one of my scripts, that modifies anything to do music files.

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import re
import os

# Spotify API credentials & playlist URL - (https://developer.spotify.com/dashboard/)

CLIENT_ID = ''
CLIENT_SECRET = ''
playlist_url = ''

# Authenticate with Spotify

auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
spotify = spotipy.Spotify(auth_manager=auth_manager)
playlist_id = playlist_url.split('/')[-1].split('?')[0]

# Fetch songs from playlist

results = spotify.playlist_items(playlist_id, additional_types=['track'])
songs = results['items']

# Path to downloads folder

downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
output_file = os.path.join(downloads_path, "playlist.txt")

# Removes invaild charcters from the song title

def remove_invaild_characters(s):
    return re.sub(r'[\\/*?:"<>|]', '', s)

# Fetch all songs from playlist (should handle playlists with more than 100 songs*) 
# It's pretty fast for 700 songs. About 8.5 seconds. - Could be faster
# Slower if spotify rate limits you.

while results['next']:
    results = spotify.next(results)
    songs.extend(results['items'])

# Save as playlist.txt file

with open(output_file, 'w', encoding='utf-8') as output_playlist:
    for index, item in enumerate(songs, start=1):
        song = item['track']
        if not song:
            continue

        # Extract and fix song info

        song_name = remove_invaild_characters(song['name'])
        artist_names = [remove_invaild_characters(artist['name']) for artist in song['artists']]
        artists = ', '.join(artist_names)

        # Write formatted line to file - Formatted like so: 1) Iris - The Goo Goo Dolls.flac

        line = str(index) + ") " + song_name + " - " + artists + ".flac\n"
        output_playlist.write(line)

print("Saved " + str(len(songs)) + " songs to " + output_file)
