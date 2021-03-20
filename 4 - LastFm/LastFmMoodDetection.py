# !/usr/bin/env python3

import argparse
import pathlib
import requests

from lastfm import lastfm_api
from genius import genius_api

BASE_URL = "http://ws.audioscrobbler.com/2.0/?method="

# Declare the script parameters.
parser = argparse.ArgumentParser(description='Analyses the mood of the given Last.Fm user based on their music consumption.')
parser.add_argument('user_id', type=str, help='The identifier of the user. Either their username or their identifier. Ex: Starkie785 - \'https://www.last.fm/user/Starkie785\'.')

args = parser.parse_args()
user = args.user_id

# Check if the provided user exists.
print(f'Retrieving information from the user \'{user}\'')

userInfo = lastfm_api.user_info(user)

if 'error' in userInfo:
    print(f"{userInfo['message']} - {user}")
    exit()

user_tracks = lastfm_api.user_tracks_from_lastweek(user)
songs_by_artist = lastfm_api.group_tracks_by_artist(user_tracks)

print(f"Found {len(user_tracks)} songs by {len(songs_by_artist)} different artists.")

lyrics_by_artist = genius_api.lyrics_by_artists(songs_by_artist)
print(lyrics_by_artist)
