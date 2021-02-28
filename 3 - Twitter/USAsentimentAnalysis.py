# !/usr/bin/env python3

import argparse
import csv
import json
import statistics
import pathlib
import pandas
import plotly.express as px

from analysis.twitter_analysis import analyse_tweets_sentiments_by_state

# Declare the script parameters.
parser = argparse.ArgumentParser(description='Analyses the sentiment on a given country from a collection of tweets.')
parser.add_argument('file', type=str, help='Path to the file containing the tweets encoded in the JSON format.')
parser.add_argument('-c', '--country', type=str, choices=["usa, spain"], help='The country to analyse the tweets from.')

args = parser.parse_args()

# Check if the given file exists.
file = pathlib.Path(args.file).resolve()

if not pathlib.Path(file).exists():
    raise FileNotFoundError(file)

country = args.country

# Process the tweets.
sentiments_by_state = analyse_tweets_sentiments_by_state(file, country)

mean_sentiment_by_state = {key: statistics.mean(value) for key, value in sentiments_by_state.items()}

fig = px.choropleth(locations=mean_sentiment_by_state.keys(), color=mean_sentiment_by_state, locationmode="USA-states", scope="usa")
fig.show()
