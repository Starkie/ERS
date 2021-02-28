# !/usr/bin/env python3

import json
import pathlib
import textblob
import time

def analyse_tweets_language_and_location(file):
    language_by_location = dict()

    with open(file, "r") as ins:
        for line in ins:
            tweet = _read_tweet(line)

            if tweet is None:
                continue

            coordinates = tweet["geo"]["coordinates"]
            if tweet["lang"]:
                language = tweet["lang"]
            else :
                language = _analyse_language(tweet["text"])

            if language_by_location.get(language) is None:
                language_by_location[language] = []

            language_by_location[language].append(coordinates)

    return language_by_location

def _read_tweet(tweet):
    if (len(tweet)> 1): ## to avoid empty lines
        data = json.loads(tweet)
        if "created_at" in data:
            if _has_coordinates(data) and "text" in data:
                return data

    return None

def _has_coordinates(tweet):
    return tweet["geo"] and tweet["geo"]["coordinates"]

def _analyse_language(text):
    return textblob.TextBlob(text).detect_language()
