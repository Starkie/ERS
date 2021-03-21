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
    song_emotions_by_artist = []

    for artist in lyrics_by_artist:
        emotions_by_song = dict()

        for song_name in artist['songs']:
            emotions_by_song[song_name] = _analyse_song_lyrics(artist['songs'][song_name])

        song_emotions_by_artist.append({'name': artist['name'], 'songs': emotions_by_song})

    return song_emotions_by_artist

def _analyse_song_lyrics(lyrics):
    clean_lyrics = _clean_lyrics(lyrics)

    # Get the top 3 emotions.
    emotion_scores = NRCLex(clean_lyrics).affect_frequencies
    sorted_song_emotions = sorted(emotion_scores, key = emotion_scores.get, reverse = True)

    # Take the 3 top emotions as the most representative of the song.
    top3_song_emotions = [emotion for emotion in sorted_song_emotions
                        if emotion != 'positive' and emotion != 'negative'][:3]

    # TODO: Take the orientation (positive or negative) separately.
    return {key: emotion_scores[key] for key in top3_song_emotions}

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
