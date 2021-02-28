# !/usr/bin/env python3

import json
import pathlib
from analysis.custom_afinn import analyse_sentiment

states_names = {'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas', 'CA': 'California', 'CO': 'Colorado',
'CT': 'Connecticut', 'DE': 'Delaware', 'FL': 'Florida', 'GA': 'Georgia', 'HI': 'Hawaii', 'ID': 'Idaho', 'IL': 'Illinois',
'IN': 'Indiana', 'IA': 'Iowa', 'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MD': 'Maryland',
'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi', 'MO': 'Missouri', 'MT': 'Montana',
'NE': 'Nebraska', 'NV': 'Nevada', 'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico', 'NY': 'New York',
'NC':'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio', 'OK': 'Oklahoma', 'OR': 'Oregon', 'PA': 'Pennsylvania',
'RI': 'Rhode Island', 'SC': 'South Carolina', 'SD': 'South Dakota', 'TN':'Tennessee', 'TX': 'Texas', 'UT': 'Utah',
'VT': 'Vermont', 'VA': 'Virginia', 'WA': 'Washington','WV': 'West Virginia', 'WI': 'Wisconsin', 'WY': 'Wyoming'}

def analyse_tweets_sentiments_by_state(file):
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

def _get_state(data):
    if data["place"] != None and data["place"]["country_code"] == "US":
        state = str(data["place"]["full_name"]).upper().split(", ")
        if len(state) > 1:
            return state[1]

def _is_state(state):
    return state in states_names.keys()
