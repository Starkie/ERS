# !/usr/bin/env python3

import plotly.express as px
import plotly.graph_objects as go
import plotly.offline as pyo
import numpy as np
import pandas as pd

def visualize_as_radar_chart(emotions_by_artist):
    categories = emotions_by_artist[0]['categories']
    categories = [cat.capitalize() for cat in categories]

    # Initialize the vector array.
    accumulated_data = [0.0] * len(categories)

    # Accumulate the emotions of each song.
    for artist in emotions_by_artist[1:]:
        for song_name in artist['songs']:
            emotions = artist['songs'][song_name]
            accumulated_data = np.add(accumulated_data, emotions)

    # Normalize the vector.
    normalized_data = accumulated_data / np.sqrt(np.sum(accumulated_data**2))

    # Plot the radar chart.
    df = pd.DataFrame(dict(
        r=normalized_data,
        theta=categories))
    fig = px.line_polar(df, r='r', theta='theta', line_close=True)

    fig.update_traces(fill='toself')

    pyo.plot(fig)
