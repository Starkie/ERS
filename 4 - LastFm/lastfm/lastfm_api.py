# !/usr/bin/env python3

import requests
import itertools
import os
from datetime import date, datetime, timedelta
from time import sleep

BASE_URL = "http://ws.audioscrobbler.com/2.0/?method="

# If no API key is provided, read it from the secrets store.
_secrets = open(os.path.join(os.path.dirname(__file__), ".secrets"))
_api_key = _secrets.read().strip()
_secrets.close()

# Base method to make calls to the Last.FM API.
def _request(method, params = ''):
    requestUrl = f"{BASE_URL}{method}{params}&api_key={_api_key}&format=json"

    return requests.get(requestUrl).json()

# Fetches the information of the given user.
def user_info(user):
    return _request('user.getinfo', params=f"&user={user}")

def user_tracks_from_lastweek(user):
    # Get the tracks from the last 7 days.
    today = date.today()
    lastWeekDate = datetime(today.year, today.month, today.day) - timedelta(days = 7)
    lastWeekDateTimeStamp = int(lastWeekDate.timestamp())

    print(f"Last.FM - Reading songs listened since '{lastWeekDate}' by '{user}'.")

    counter = 0
    tracks = []

    # Iterate over the paged query.
    for i in itertools.count(1):
        response = _request('user.getRecentTracks', params=f"&user={user}&from={lastWeekDateTimeStamp}&page={i}")

        if 'error' in response:
            print(response['message'])
            return

        recent_tracks = response['recenttracks']

        # Get the tracks excluding the track currently playing.
        new_tracks =  [track for track in recent_tracks['track'] if '@attr' not in track]
        tracks.extend(new_tracks)

        counter += len(new_tracks)
        total = int(recent_tracks['@attr']['total'])
        print(f"Last.FM - Read {counter} out of {total} tracks.")

        if counter >= total:
            break

        # Rate limit the requests to the API.
        sleep(5)

    return tracks

# Groups the tracks by unique artist.
def group_tracks_by_artist(tracks):
    songs_by_artist = dict()

    for song in tracks:
        name = song['name']
        artist = song['artist']
        date_listened = datetime.fromtimestamp(int(song['date']['uts']))

        # Use the ID to avoid collisions of artists with the same name.
        # Sometimes the mbid is not filled out. Use the artists name instead.
        artist_id = artist['mbid'] if artist['mbid'] else artist['#text']

        if artist_id not in songs_by_artist:
            songs_by_artist[artist_id] = {"name": artist['#text'], "songs": {}}

        if name not in songs_by_artist[artist_id]['songs']:
            songs_by_artist[artist_id]['songs'][name] = []

        # Store the date and time when the track was listened.
        songs_by_artist[artist_id]['songs'][name].append(date_listened)

    return songs_by_artist
