# !/usr/bin/env python3

import argparse
import pathlib
from analysis.twitter_analysis import analyse_tweets_language_and_location
import plotly.express as px
import plotly.graph_objects as go

# Declare the script parameters.
parser = argparse.ArgumentParser(description='Analyses the languages written on a given tweet collection from Spain.')
parser.add_argument('file', type=str, help='Path to the file containing the tweets encoded in the JSON format.')

args = parser.parse_args()

# Check if the given file exists.
file = pathlib.Path(args.file).resolve()

if not pathlib.Path(file).exists():
    raise FileNotFoundError(file)

locations_by_language = analyse_tweets_language_and_location(file)

fig = go.Figure()

for language in locations_by_language:
    latitudes = [coordinates[0] for coordinates in locations_by_language[language]]
    longitudes = [coordinates[1] for coordinates in locations_by_language[language]]

    fig.add_trace(go.Scattergeo(
        locationmode = 'country names',
        # lon = df_sub['lon'],
        # lat = df_sub['lat'],
        lat=latitudes,
        lon=longitudes,
        text = language,
        marker = dict(
            # size = df_sub['pop']/scale,
            # color = colors[i],
            line_width=0.5,
            sizemode = 'area'
        ),
        name = language))

    fig.update_layout(
        title_text = 'Tweets by language in Spain',
        showlegend = True,
        geo = dict(
            scope = 'europe',
            landcolor = 'rgb(217, 217, 217)',
        )
    )

fig.show()
