# !/usr/bin/env python3

import lyricsgenius
import os
from time import sleep

secrets = open(os.path.join(os.path.dirname(__file__), ".secrets"))
api_key = secrets.read().strip()
genius_API = lyricsgenius.Genius(api_key)

def lyrics_by_artists(songs_by_artist):
    lyrics_by_artist = []

    for key in songs_by_artist:
        lyrics_by_artist.append(_get_artist_lyrics(songs_by_artist[key]))

    return lyrics_by_artist

def _get_artist_lyrics(artist_songs):
    artist_name = artist_songs['name']
    artist_lyrics = {"name": artist_name, "songs":dict()}

    # Convert the songs to a set to a avoid duplication.
    for song in set(artist_songs['songs']):
        # Search by the artist and song to avoid incorrect results.
        found_song = genius_API.search_song(f"{artist_name} {song}")

        if found_song != None:
            artist_lyrics['songs'][song] = found_song.lyrics

        # Add waits to ratelimit the requests.
        sleep(3)

    return artist_lyrics
