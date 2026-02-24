# Author: MythbladeStudios
# Date Created: 10 / 31 / 2025
# Date Modified: 02 / 23 / 2026
# Description: Converts a spotify playlist into a txt file which you can use 
# with another one of my scripts, that modifies metadata for audio files.

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import re
import os
import time

# Spotify API credentials & playlist URL - (https://developer.spotify.com/dashboard/)

CLIENT_ID = ''
CLIENT_SECRET = ''
playlist_url = ''

# Audio file format - (https://en.wikipedia.org/wiki/Audio_file_format#list)

file_extension = '.flac'
include_url = False

# Start timer - Speedrun timer goes brrr :D

start_time = time.time()

# Authenticate with Spotify

auth_manager = SpotifyClientCredentials(client_id = CLIENT_ID, client_secret = CLIENT_SECRET)
spotify      = spotipy.Spotify(auth_manager = auth_manager)
playlist_id  = playlist_url.split('/')[-1].split('?')[0]

# Fetch all songs from playlist

results = spotify.playlist_items(
    playlist_id,
    fields = 'items(track(id,name,artists(name))),next',
    additional_types = ['track'])

songs = results['items']

# Path to downloads folder

downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
output_file    = os.path.join(downloads_path, "playlist.txt")

# Pre-compile regex filter for invalid characters

INVALID_CHARACTERS_FILTER = re.compile(r'[\\*?:"<>|]')

# Remove invalid characters from song title

def remove_invalid_characters(s):
    return INVALID_CHARACTERS_FILTER.sub('', s)

# Fetch songs from playlist

while results['next']:
    results = spotify.next(results)
    songs.extend(results['items'])

# Remove deleted and or unavailable tracks

songs = [item for item in songs if item.get('track')]

# Save as playlist.txt file

lines = []
for index, item in enumerate(songs, start=1):
    song         = item['track']
    song_name    = remove_invalid_characters(song['name'])
    artist_names = [remove_invalid_characters(artist['name']) for artist in song['artists']]
    artists      = ', '.join(artist_names)

    # Write formatted line - Formatted like so: 1) Iris - The Goo Goo Dolls.flac | https://open.spotify.com/track/...

    if include_url:
        track_url = f"https://open.spotify.com/track/{song['id']}"
        lines.append(f"{index}) {song_name} - {artists}{file_extension} | {track_url}\n")

    else:
        lines.append(f"{index}) {song_name} - {artists}{file_extension}\n")

with open(output_file, 'w', encoding='utf-8') as output_playlist:
    output_playlist.writelines(lines)

# Calculate runtime - Yippie!
# Pretty fast for 700 songs (~5.4 seconds)
# Slower if Spotify rate limits you :(

end_time     = time.time()
runtime      = end_time - start_time
seconds      = int(runtime)
milliseconds = int((runtime % 1) * 1000)

print(f"\n[Info] - Saved {len(songs)} songs to {output_file}")
print(f"         Total runtime: {seconds} seconds and {milliseconds} milliseconds")
