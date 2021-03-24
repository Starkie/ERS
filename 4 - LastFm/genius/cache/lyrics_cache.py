# !/usr/bin/env python3

import sqlite3
import os.path

from contextlib import closing

_database_name = 'lyrics.db'
_connection = None

_CREATE_TABLE_LYRICS = 'CREATE TABLE lyrics (artist text, song_name text, lyrics text)'
_SEARCH_LYRICS_QUERY = 'SELECT * FROM LYRICS WHERE ARTIST = ? AND SONG_NAME = ?'
_INSERT_LYRICS_QUERY = 'INSERT INTO LYRICS VALUES(?,?,?)'

def get_lyrics(artist, song_name):
    cursor = _cursor()

    try:
        params = (artist, song_name)
        cursor.execute(_SEARCH_LYRICS_QUERY, params)

        return cursor.fetchone()
    finally:
        cursor.close()

def store_lyrics(artist, song_name, lyrics):
    cursor = _cursor()

    try:
        params = (artist, song_name, lyrics)
        cursor.execute(_INSERT_LYRICS_QUERY, params)
        _connection.commit()
    finally:
        cursor.close()

def _cursor():
    if _connection:
        return _connection.cursor()

    return _connect(_database_name).cursor()

def _connect(_database_name):
    database_exists = os.path.exists(_database_name)

    global _connection
    _connection = sqlite3.connect(_database_name)

    if not database_exists:
        _initialize_database(_connection, _database_name)

    return _connection

def _initialize_database(connection, database_name):
    cursor = connection.cursor()

    try:
        cursor.execute(_CREATE_TABLE_LYRICS)
        connection.commit()
    finally:
        cursor.close()
