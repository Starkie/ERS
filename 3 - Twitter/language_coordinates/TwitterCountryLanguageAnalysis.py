# !/usr/bin/env python3

import argparse
import pathlib
import plotly.express as px
import plotly.graph_objects as go
from analysis.twitter_analysis import analyse_tweets_language_and_location

# Declare the script parameters.
parser = argparse.ArgumentParser(description='Analyses the languages written on a given tweet collection from Spain.')
parser.add_argument('file', type=str, help='Path to the file containing the tweets encoded in the JSON format.')

args = parser.parse_args()

# Check if the given file exists.
file = pathlib.Path(args.file).resolve()

if not pathlib.Path(file).exists():
    raise FileNotFoundError(file)

# Analyse the dataset.
locations_by_language = analyse_tweets_language_and_location(file)

# Create the map.
fig = go.Figure()

fig.update_layout(
    title_text = 'Tweets by language in Spain',
    showlegend = True,
    geo = dict(
        scope = 'europe',
        landcolor = 'rgb(217, 217, 217)',

        # Center the map in Madrid.
        center = dict(
            lat=40.416667,
            lon=-3.716667
        ),

        # Clip the axis to only show Spain.
        lonaxis=dict(
            range=[-10, 4]
        ),
        lataxis=dict(
            range=[34, 45]
        )
    )
)

# Display the data.
for language in locations_by_language:
    latitudes = [coordinates[0] for coordinates in locations_by_language[language]]
    longitudes = [coordinates[1] for coordinates in locations_by_language[language]]

    fig.add_trace(go.Scattergeo(
        locationmode = 'country names',
        lat=latitudes,
        lon=longitudes,
        text = language,
        marker = dict(
            line_width=0.5,
            sizemode = 'area'
        ),
        name = language))

fig.show()
