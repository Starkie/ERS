# !/usr/bin/env python3

import lyricsgenius
import os
from time import sleep

# If no API key is provided, read it from the secrets store.
_secrets = open(os.path.join(os.path.dirname(__file__), ".secrets"))
_api_key = _secrets.read().strip()
genius_API = lyricsgenius.Genius(_api_key)
genius_API.verbose = False

def lyrics_by_artists(songs_by_artist):
    lyrics_by_artist = []

    for key in songs_by_artist:
        artist_lyrics = _get_artist_lyrics(songs_by_artist[key])

        if artist_lyrics != None:
            lyrics_by_artist.append(artist_lyrics)

    return lyrics_by_artist

def _get_artist_lyrics(artist_songs):
    artist_name = artist_songs['name']
    artist_lyrics = {"name": artist_name, "songs":dict()}

    print(f"Genius - Searching lyrics of '{artist_name}'.")

    # Convert the songs to a set to a avoid duplication.
    for song in set(artist_songs['songs']):
        # Search by the artist and song to avoid incorrect results.
        found_song = genius_API.search_song(f"{artist_name} {song}")

        if found_song != None:
            artist_lyrics['songs'][song] = found_song.lyrics
        else:
            print(f"Genius - The song '{artist_name} - {song}' was not found.")

        # Add waits to ratelimit the requests.
        sleep(3)

    # If no lyrics for the song were found, the artist should not be considered.
    # This is usually the case for artists with only instrumental songs.
    if len(artist_lyrics['songs']) == 0:
        return None

    return artist_lyrics
