import nltk
import numpy as np
import pandas as pd
import re
import string
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
            emotions_by_song[song_name] = _analyse_song_lyrics(artist['songs'][song_name])

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

def normalize_user_emotions(song_emotions_by_artist):
    # Initialize the vector array.
    accumulated_data = [0.0] * len(emotions)

    # Accumulate the emotions of each song.
    for artist in song_emotions_by_artist[1:]:
        for song_name in artist['songs']:
            song_emotions = artist['songs'][song_name]
            accumulated_data = np.add(accumulated_data, song_emotions)

    # Normalize the vector.
    normalized_data = accumulated_data / np.sqrt(np.sum(accumulated_data**2))

    return normalized_data.tolist()
