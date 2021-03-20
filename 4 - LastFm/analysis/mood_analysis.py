import nltk
import re
import string
from nrclex import NRCLex, top_emotions, build_word_affect

# NLTK tokens required by NRCLex
nltk.download("brown")
nltk.download("punkt")

# Stopwords to clean the lyrics.
nltk.download("stopwords")
stopwords = set(nltk.corpus.stopwords.words('english'))

def analyse_lyrics(lyrics_by_artist):
    for lyrics in lyrics_by_artist:
        for song_name in lyrics['songs']:
            _analyse_song_lyrics(lyrics['songs'][song_name])

def _analyse_song_lyrics(lyrics):
    clean_lyrics = _clean_lyrics(lyrics)

    emotion_analyser = NRCLex(clean_lyrics)

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

    for char in '“”' + string.punctuation:
        res = res.replace(char, " ")

    return res
