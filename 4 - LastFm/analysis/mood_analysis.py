import nltk
import numpy as np
import pandas as pd
import re
import string
from nrclex import NRCLex, top_emotions, build_word_affect

# NLTK tokens required by NRCLex
nltk.download("brown")
nltk.download("punkt")

# The categories that NRCLex uses to categorize words.
emotions = ['joy', 'trust', 'fear', 'surprise', 'sadness', 'disgust', 'anger', 'anticipation']

# Stopwords to clean the lyrics.
nltk.download("stopwords")
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
    sorted_song_emotions = sorted(emotion_scores, key = emotion_scores.get, reverse = True)

    # Take the 3 top emotions as the most representative of the song.
    top3_song_emotions = [emotion for emotion in sorted_song_emotions
                          if emotion != 'positive' and emotion != 'negative'][:3]

    # The orientation (positive or negative) is considered separately.
    # TODO: Include the orientation in the result.
    # orientation = 'positive' if (emotion_scores['positive'] >= emotion_scores['negative']) else 'negative'

    # Use the categories to create the row of the song.
    return [emotion_scores[emotion] if (emotion in top3_song_emotions) else 0.0
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

def normalize_emotions_by_artist(song_emotions_by_artist):
    # Initialize the vector array.
    accumulated_data = [0.0] * len(emotions)

    # Accumulate the emotions of each song.
    for artist in song_emotions_by_artist[1:]:
        for song_name in artist['songs']:
            song_emotions = artist['songs'][song_name]
            accumulated_data = np.add(accumulated_data, song_emotions)

    # Normalize the vector.
    normalized_data = accumulated_data / np.sqrt(np.sum(accumulated_data**2))

    categories = [emo.capitalize() for emo in emotions]

    dataframe = pd.DataFrame(dict(
        r=normalized_data,
        categories=categories))

    return dataframe
