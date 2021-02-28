# !/usr/bin/env python3

import argparse
import csv
import json
import statistics
import pathlib
import pandas
import plotly.express as px

from analysis.tweet_afinn import analyse_sentiment

states_names = {'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas', 'CA': 'California', 'CO': 'Colorado',
'CT': 'Connecticut', 'DE': 'Delaware', 'FL': 'Florida', 'GA': 'Georgia', 'HI': 'Hawaii', 'ID': 'Idaho', 'IL': 'Illinois',
'IN': 'Indiana', 'IA': 'Iowa', 'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MD': 'Maryland',
'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi', 'MO': 'Missouri', 'MT': 'Montana',
'NE': 'Nebraska', 'NV': 'Nevada', 'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico', 'NY': 'New York',
'NC':'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio', 'OK': 'Oklahoma', 'OR': 'Oregon', 'PA': 'Pennsylvania',
'RI': 'Rhode Island', 'SC': 'South Carolina', 'SD': 'South Dakota', 'TN':'Tennessee', 'TX': 'Texas', 'UT': 'Utah',
'VT': 'Vermont', 'VA': 'Virginia', 'WA': 'Washington','WV': 'West Virginia', 'WI': 'Wisconsin', 'WY': 'Wyoming'}

def _get_state(data):
    if data["place"] != None and data["place"]["country_code"] == "US":
        state = str(data["place"]["full_name"]).upper().split(", ")
        if len(state) > 1:
            return state[1]

def _is_state(state):
    return state in states_names.keys()

def _analyse_tweets_sentiments_by_state(file):
    sentiments_by_state = dict()

    with open(file, "r") as ins:
        for line in ins:
            state_text = _read_tweet(line)

            if state_text is None:
                continue

            (state, text) = state_text

            sentiment = analyse_sentiment(text)

            if sentiments_by_state.get(state) is None:
                sentiments_by_state[state] = []

            sentiments_by_state[state].append(sentiment)

    return sentiments_by_state

def _read_tweet(tweet):
    if (len(tweet)> 1): ## to avoid empty lines
        data = json.loads(tweet)

        if "created_at" in data:
            state = _get_state(data)

            if _is_state(state) and "text" in data:
                return (state, data["text"])

    return None

# Declare the script parameters.
parser = argparse.ArgumentParser(description='Analyses the sentiment on a given country from a collection of tweets.')
parser.add_argument('file', type=str, help='Path to the file containing the tweets encoded in the JSON format.')
parser.add_argument('-c', '--country', type=str, choices=["usa"], help='The country to analyse the tweets.')

args = parser.parse_args()

# Check if the given file exists.
file = pathlib.Path(args.file).resolve()

if not pathlib.Path(file).exists():
    raise FileNotFoundError(file)

# Process the tweets.
sentiments_by_state = _analyse_tweets_sentiments_by_state(file)

mean_sentiment_by_state = {key: statistics.mean(value) for key, value in sentiments_by_state.items()}

fig = px.choropleth(locations=mean_sentiment_by_state.keys(), color=mean_sentiment_by_state, locationmode="USA-states", scope="usa")
fig.show()
