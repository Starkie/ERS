import nltk
import numpy as np
import pandas as pd
import re
import string

from datetime import date, datetime, timedelta
from nrclex import NRCLex, top_emotions, build_word_affect

# NLTK tokens required by NRCLex
nltk.download("brown", quiet = True)
nltk.download("punkt", quiet = True)

# The categories that NRCLex uses to categorize words.
emotions = ['joy', 'trust', 'fear', 'surprise', 'sadness', 'disgust', 'anger', 'anticipation']

# Stopwords to clean the lyrics.
nltk.download("stopwords", quiet = True)
stopwords = set(nltk.corpus.stopwords.words('english'))

def analyse_lyrics(lyrics_by_artist):
    song_emotions_by_artist = [{ "categories": emotions }]

    for artist in lyrics_by_artist:
        emotions_by_song = dict()

        for song_name in artist['songs']:
            song = artist['songs'][song_name]
            song_emotions = _analyse_song_lyrics(song['lyrics'])
            emotions_by_song[song_name] = {'emotions': song_emotions, 'date_listened': song['date_listened']}

        song_emotions_by_artist.append({'name': artist['name'], 'songs': emotions_by_song})

    return song_emotions_by_artist

def _analyse_song_lyrics(lyrics):
    lyrics_keywords = _clean_lyrics(lyrics)

    # Analyse the emotions of the song lyrics.
    emotion_scores = NRCLex(lyrics_keywords).affect_frequencies

    # Use the categories to create the row of the song.
    return [emotion_scores[emotion] if (emotion in emotion_scores) else 0.0
            for emotion in emotions]

def _clean_lyrics(lyrics):
    # Remove the verse markers from Genius.
    # Example: [Verse 1]
    removed_markers = re.sub(r'\[.*\]', '', lyrics)

    # Remove text punctuation.
    clean_lyrics = _remove_punctuation(removed_markers)

    split_lyrics = clean_lyrics.split()
    lower_split = [word.lower() for word in split_lyrics]

    # Remove stopwords.
    lyrics_keywords = [word for word in lower_split if word not in stopwords]

    # Returns the keywords as a string.
    return " ".join(lyrics_keywords)


def _remove_punctuation(content):
    res = content

    for char in '“”’' + string.punctuation:
        res = res.replace(char, " ")

    return res

def normalize_user_emotions(song_emotions_by_artist, start_date):
    days_emotions = _initialize_days_emotions(start_date)

    # Accumulate the emotions of each song.
    for artist in song_emotions_by_artist[1:]:
        for song_name in artist['songs']:
            song = artist['songs'][song_name]
            song_emotions = song['emotions']

            for date_listen in song['date_listened']:
                date_str = date_listen.strftime("%d/%m/%Y")
                days_emotions[date_str] = np.add(days_emotions[date_str], song_emotions)

    total = [0.0] * len(emotions)

    for day in days_emotions:
        total = np.add(total, days_emotions[day])

        # Normalize the already used vector.
        days_emotions[day] = _normalize_vector(days_emotions[day])

    total = _normalize_vector(total)

    return {'days': days_emotions, 'total': total}

def _initialize_days_emotions(start_date):
    today = datetime.today()

    num_days = (today - start_date).days + 1
    days_list = [today - timedelta(days=x) for x in range(num_days)]

    days_emotions = { day.strftime("%d/%m/%Y") : [0.0] * len(emotions) for day in days_list}

    return days_emotions

def _normalize_vector(data):
    if np.count_nonzero(data) == 0:
        return data

    normalized_data = data / np.sqrt(np.sum(data**2))

    return normalized_data.tolist()
