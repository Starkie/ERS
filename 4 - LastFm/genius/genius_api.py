# !/usr/bin/env python3

import lyricsgenius
import os

from genius.cache import lyrics_cache

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
        found_lyrics = _get_song_lyrics(artist_name, song)

        if found_lyrics:
            artist_lyrics['songs'][song] = {'lyrics':found_lyrics, 'date_listened': artist_songs['songs'][song]}

    # If no lyrics for the song were found, the artist should not be considered.
    # This is usually the case for artists with only instrumental songs.
    if len(artist_lyrics['songs']) == 0:
        return None

    return artist_lyrics

def _get_song_lyrics(artist, song):
    try:
        cached_lyrics = lyrics_cache.get_lyrics(artist, song)

        if cached_lyrics:
            return cached_lyrics[2]

        # Search by the artist and song to avoid incorrect results.
        found_song = genius_API.search_song(f"{artist} {song}")

        # Check that the artist of the found song matches the expected one.
        if found_song != None and found_song.artist.lower() == artist.lower() :
            lyrics_cache.store_lyrics(artist, song, found_song.lyrics)

            # Add waits to ratelimit the requests.
            sleep(3)

            return found_song.lyrics
    except Exception as ex:
        print(ex)
        print('Genius - Connection timed out.')

    print(f"Genius - The song '{artist} - {song}' was not found.")

    return None

