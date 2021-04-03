# !/usr/bin/env python3

import argparse

from datetime import date, datetime, timedelta

from lastfm import lastfm_api
from genius import genius_api
from analysis import mood_analysis
from visualization import emotion_visualization

# Declare the script parameters.
parser = argparse.ArgumentParser(description='Analyses the mood of the given Last.Fm users based on their music consumption.')
parser.add_argument('user_id', action='append', nargs='+', help='One or more identifiers of Last.FM users. Either their username or their identifier. Ex: Starkie785 - \'https://www.last.fm/user/Starkie785\'.')

def _is_valid_lastfm_user(user):
    userInfo = lastfm_api.user_info(user)

    if 'error' in userInfo:
        return None

    return user

def _analyse_lastfm_user(user, start_date):
    user_tracks = lastfm_api.user_tracks_from_date(user, start_date)
    songs_by_artist = lastfm_api.group_tracks_by_artist(user_tracks)

    print(f"Found {len(user_tracks)} songs by {len(songs_by_artist)} different artists.")

    lyrics_by_artist = genius_api.lyrics_by_artists(songs_by_artist)

    song_emotions_by_artist = mood_analysis.analyse_lyrics(lyrics_by_artist)
    user_emotions = mood_analysis.normalize_user_emotions(song_emotions_by_artist, start_date)

    return user_emotions

# Parse the given Last.fm users.
args = parser.parse_args()
users = args.user_id[0]

emotion_by_user = dict()

# Get the tracks from the last 7 days.
today = date.today()
lastWeekDate = datetime(today.year, today.month, today.day) - timedelta(days = 7)

# Analyse the provided users
for user in users:
    # Check if the provided user exists.
    print(f'Retrieving information from the user \'{user}\'')

    if not _is_valid_lastfm_user(user):
        print(f"'{user}' is not a valid Last.FM user.")

        continue

    user_emotions = _analyse_lastfm_user(user, lastWeekDate)
    emotion_by_user[user] = user_emotions

if len(emotion_by_user) == 0:
    print("No valid user provided.")
    exit()

if len(users) > 1:
    emotion_visualization.visualize_as_proximity_matrix(emotion_by_user, mood_analysis.emotions)

for user in emotion_by_user:
    emotion_visualization.visualize_as_time_series(user, emotion_by_user[user], mood_analysis.emotions)

emotion_visualization.visualize_as_radar_chart(emotion_by_user, mood_analysis.emotions)
