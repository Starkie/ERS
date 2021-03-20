# !/usr/bin/env python3

import requests
import itertools
from datetime import date, datetime, timedelta
from time import sleep

BASE_URL = "http://ws.audioscrobbler.com/2.0/?method="

# Base method to make calls to the Last.FM API.
def _request(method, api_key, params = ''):
    requestUrl = f"{BASE_URL}{method}{params}&api_key={api_key}&format=json"

    return requests.get(requestUrl).json()

# Fetches the information of the given user.
def user_info(user, api_key):
    return _request('user.getinfo', api_key, params=f"&user={user}")

def user_tracks_from_lastweek(user, api_key):
    # Get the tracks from the last 7 days.
    today = date.today()
    lastWeekDate = datetime(today.year, today.month, today.day) - timedelta(days = 7)
    lastWeekDateTimeStamp = int(lastWeekDate.timestamp())

    counter = 0
    tracks = []

    # Iterate over the paged query.
    for i in itertools.count(1):
        response = _request('user.getRecentTracks', api_key, params=f"&user={user}&from={lastWeekDateTimeStamp}&page={i}")

        if 'error' in response:
            print(response['message'])
            return

        recent_tracks = response['recenttracks']

        # Get the tracks excluding the track currently playing.
        new_tracks =  [track for track in recent_tracks['track'] if '@attr' not in track]
        tracks.extend(new_tracks)

        counter += len(new_tracks)
        print(f"Read {counter} out of {recent_tracks['@attr']['total']} tracks.")

        # If the obtained page has less than 50 tracks, we have reached the end.
        if len(new_tracks) < 50:
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

        # Use the ID to avoid collisions of artists with the same name.
        # Sometimes the mbid is not filled out. Use the artists name instead.
        artist_id = artist['mbid'] if artist['mbid'] else artist['#text']

        if artist_id not in songs_by_artist:
            songs_by_artist[artist_id] = {"name": artist['#text'], "songs": []}

        songs_by_artist[artist_id]['songs'].append(name)

    return songs_by_artist
